import importlib


class WriterTensorboardX():
    def __init__(self, writer_dir, logger, enable):
        self.writer = None
        if enable:
            log_path = str(writer_dir)
            try:
                self.writer = importlib.import_module('tensorboardX').SummaryWriter(log_path)
            except ImportError:
                message = "Warning: TensorboardX visualization is configured to use, but currently not installed on " \
                    "this machine. Please install the package by 'pip install tensorboardx' command or turn " \
                    "off the option in the 'config.json' file."
                logger.warning(message)
        self.step = 0
        self.mode = ''

        self.tb_writer_ftns = [
            'add_scalar', 'add_scalars', 'add_image', 'add_images', 'add_audio',
            'add_text', 'add_histogram', 'add_pr_curve', 'add_embedding'
        ]
        self.tag_mode_exceptions = ['add_histogram', 'add_embedding']


    def set_step(self, step, mode='train'):
        self.mode = mode
        self.step = step

    def __getattr__(self, name):
        """
        If visualization is configured to use:
            return add_data() methods of tensorboard with additional information (step, tag) added.
        Otherwise:
            return a blank function handle that does nothing
        """
        if name in self.tb_writer_ftns:
            add_data = getattr(self.writer, name, None)

            def wrapper(tag, data, *args, **kwargs):
                if add_data is not None:
                    # add mode(train/valid) tag
                    if name not in self.tag_mode_exceptions:
                        tag = '{}/{}'.format(self.mode, tag)
                    add_data(tag, data, self.step, *args, **kwargs)
            return wrapper
        else:
            # default action for returning methods defined in this class, set_step() for instance.
            try:
                attr = object.__getattr__(name)
            except AttributeError:
                raise AttributeError("type object 'WriterTensorboardX' has no attribute '{}'".format(name))
            return attr
