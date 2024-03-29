class FreezeInfo(object):
    """
    Main interface around wrappers
    """

    def __init__(self):
        """
        It is not clear yet howto manage the switch between pip ou buildout
        wrapper.

        It may probably not automatic since the buildout code will need a
        path to scan for Eggs.

        Pip wrapper should not need any argument, but the buildout one will
        need this "eggs" path.

        Finally, the wrapper modules should not be loaded from global level
        since each one could need to import specific module (like pip or
        zc.buildout) that may bo available for opposed environment.

        Tips: zc.buildout is installed in site-package
        on every buildout project, it may be useful to automatically detect
        Buildout install (and if not installed, we could switch to pip as
        default). However it may be difficult to include zc.buildout install
        or not through test environments (We don't want it as this application
        requirement).
        """
        self.wrapper = None

    def infos(self):
        """
        Return package versions informations

        Returns:
            dict: Package items.
        """
        raise NotImplementedError
        # return self.wrapper.output()
