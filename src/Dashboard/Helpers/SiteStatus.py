import os

class SiteStatus:

    def enable(self):
        self.__rename(old="index.html", new="updating_data.html")
        self.__rename(old="index-original.html", new="index.html")

    def updatingData(self):
        self.__rename(old="index.html", new="index-original.html")
        self.__rename(old="updating_data.html", new="index.html")

    def __rename(self, old, new):
        from_name = self.__buildFrontendPath(old)
        to_name = self.__buildFrontendPath(new)
        os.rename(from_name, to_name)

    def __buildFrontendPath(self, filename):
        frontend_dir = os.getenv('FRONTEND_DIR')
        concat = os.getenv('PATH_CONCAT')
        return "{}{}{}".format(frontend_dir, concat, filename)