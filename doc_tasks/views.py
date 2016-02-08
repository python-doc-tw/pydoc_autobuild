from collections import namedtuple

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.http import Http404, HttpResponse
from django.utils.timezone import activate
from django_q.tasks import async, Task
from django_q.models import OrmQ


ParsedCompletedCommand = namedtuple('ParsedCompletedCommand',
                                    ['returncode', 'stdout', 'stderr'])


def decode_cmd_out(completed_cmd):
    try:
        stdout = completed_cmd.stdout.decode()
    except AttributeError:
        stdout = '<EMPTY>'
    try:
        stderr = completed_cmd.stderr.decode()
    except AttributeError:
        stderr = '<EMPTY>'
    return ParsedCompletedCommand(
        completed_cmd.returncode,
        stdout,
        stderr
    )


@require_GET
def run_task_update_one_source(request):
    source_path = request.GET.get('source_path', None)
    if source_path is None:
        raise Http404('No given source_path')
    task_id = async('doc_tasks.tasks.update_one_page', page=source_path)
    return HttpResponse(
        'Submitted as task %s. See <a href="%s">task queue</a>.'
        % (task_id, reverse('home'))
    )


@require_GET
def view_task(request, id):
    task = get_object_or_404(Task, id=id)
    result = task.result
    if task.func == 'doc_tasks.tasks.update_one_page':
        tx_pull = decode_cmd_out(result['tx_pull'])
        sphinx_intl_build = decode_cmd_out(result['sphinx_intl_build'])
        sphinx_build_html = decode_cmd_out(result['sphinx_build_html'])
        return render(request, 'one_page_task.html', {
            'task': task,
            'tx_pull': tx_pull,
            'sphinx_intl_build': sphinx_intl_build,
            'sphinx_build_html': sphinx_build_html,
        })
    return Http404(
        'Given task of type %s does not have the result template '
        'to be rendered yet.'
        % task.func
    )


@require_GET
def home(request):
    tz = 'Asia/Taipei'
    activate(tz)
    queued_tasks = OrmQ.objects.all().order_by('lock')
    one_page_tasks = Task.objects.all().filter(
        func__exact='doc_tasks.tasks.update_one_page'
    ).order_by('-started')
    return render(request, 'index.html', {
        'one_page_tasks': one_page_tasks,
        'queued_tasks': queued_tasks,
        'tz': tz,
    })
