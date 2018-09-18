import click


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx, threads, keyfile, input_file, respect_word_order, **kwargs):
    pass

if __name__ == '__main__':
        main()
