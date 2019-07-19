import os

from collections import OrderedDict


class BuildoutInfo(object):
    """
    Information about 
    """
    def __init__(self, path=None):
        self.path = path # path to scan for Eggs
        self.egginfo_dir = 'EGG-INFO'
        self.requirement_filename = 'requires.txt'
        self.eggname_filter = lambda name: not name.startswith('.') and name.endswith('.egg')

    def output(self):
        eggs = OrderedDict()

        # List all egg in directory
        for egg_name in os.listdir(self.path):
            egg_dir = os.path.join(self.path, egg_name)
            # Valid egg names
            if os.path.isdir(egg_dir) and self.eggname_filter(egg_name):
                egginfo_dir = os.path.join(egg_dir, self.egginfo_dir)
                
                # Search throught egg-info dir for a requirement file if any
                if os.path.exists(egginfo_dir):
                    requirement_filepath = os.path.join(
                        egginfo_dir, self.requirement_filename)
                    if os.path.exists(requirement_filepath):
                        reqs = []
                        # Naively parse requirements
                        with open(requirement_filepath, 'rb') as requirement_file:
                            content = requirement_file.read()
                            for line in content.splitlines():
                                # Dont retain extra requirements
                                if line and line.startswith(b'['):
                                    break
                                elif line:
                                    reqs.append(line)
                        if len(line)>0:
                            eggs[egg_name] = reqs
                    #else:
                        #print "* No provided requirements"
        return eggs
