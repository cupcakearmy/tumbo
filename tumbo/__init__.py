from tumbo.tumbo import login_if_required, compile_templates, process_queue


def runner(context, variables, recipe, tag=None, registry=None, parallel=True, push=False, run=False):
    host = login_if_required(registry)

    queue = compile_templates(variables, recipe, tag, context)
    if host:
        queue = [
            (rendered, f'{host}/{tag}')
            for rendered, tag in queue
        ]

    process_queue(
        queue,
        context,
        parallel=parallel,
        push=push,
        run=run,
    )
