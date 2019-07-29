from collections import OrderedDict

try:
    from pip._internal.operations import freeze
except ImportError: # pip < 10.0
    from pip.operations import freeze

PACKAGES = list(freeze.freeze())

class PipInfo(object):
    """
    Pip wrapper
    """
    def output(self):
        output_dict = OrderedDict()
        for package in PACKAGES:
            try:
                name, version = package.split('==')
                output_dict[name] = version
            except ValueError:
                # What should we do if the value doesn't have a version?
                continue
        return output_dict
