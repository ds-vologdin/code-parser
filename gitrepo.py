from git import Repo
import shutil


class GitRepo:
    """ Класс для работы с git репозиторием """
    def __init__(self, git_url, to_dir='/tmp/', branch='master'):
        self.git_url = git_url
        if not git_url:
            to_dir = ''
        if to_dir == '/tmp/':
            to_dir += git_url.split('/')[-1].replace('.git', '') + '/'
        self.local_path = to_dir
        self.branch = branch
        self.is_cloned = False

    def clone_git_url(self):
        ''' Возвращает путь до каталога, куда был клонирован репозиторий
        В случае ошибки возвращает пустую строку '''
        if not self.git_url:
            return ''
        try:
            Repo.clone_from(
                self.git_url, self.local_path, branch=self.branch
            )
            self.is_cloned = True
        except:
            self.remove_local_git_repo()
            self.local_path = ''
            self.is_cloned = False
        return self.local_path

    def remove_local_git_repo(self):
        ''' Удаление локального репозитория. Возвращает в случае успеха True,
        иначе False '''
        if (not self.local_path or self.local_path == '/tmp/'):
            return False
        if not self.is_cloned:
            return False
        try:
            shutil.rmtree(self.local_path)
            self.is_cloned = False
        except:
            return False
        return True
