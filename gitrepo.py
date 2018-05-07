from git import Repo
import shutil


class GitRepo:
    """ Класс для работы с git репозиторием """
    def __init__(self, git_url, to_dir='/tmp/', branch='master'):
        self.git_url = git_url
        if to_dir == '/tmp/':
            to_dir += git_url.split('/')[-1].replace('.git', '') + '/'
        self.local_path = to_dir
        self.branch = branch

    def clone_git_url(self):
        try:
            Repo.clone_from(
                self.git_url, self.local_path, branch=self.branch
            )
        except:
            self.remove_local_git_repo()
            self.local_path = ''
        return self.local_path

    def remove_local_git_repo(self):
        try:
            shutil.rmtree(self.local_path)
        except:
            return False
        return True
