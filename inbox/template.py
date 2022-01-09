import os

FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(FILE_PATH)
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


class Template:
    template_name = ""
    context = None

    def __init__(self, template_name="", context=None):
        self.template_name = template_name
        self.context = context

    def get_template(self):
        template_path = os.path.join(TEMPLATE_DIR, self.template_name)
        if not os.path.exists(template_path):
            raise Exception("This file doesn't exist")
        template_str = ""
        with open(template_path, "r") as f:
            template_str = f.read()
        return template_str

    def render(self, context=None):
        render_ctx = {}
        template_str = self.get_template()

        if self.context is not None:
            render_ctx = self.context
        else:
            render_ctx = context

        # unpack dict
        return template_str.format(**render_ctx)
