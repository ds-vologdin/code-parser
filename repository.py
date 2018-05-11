from git import Repo
import shutil


class Repository:
    """ Прототип классов для работы с репозиториями (git, mercurial и т.д.) """
    def __init__(self, git_url, to_dir='/tmp/', branch='master'):
        self.git_url = git_url
        if not git_url:
            to_dir = ''
        if to_dir == '/tmp/':
            to_dir += git_url.split('/')[-1].replace('.git', '') + '/'
        self.local_path = to_dir
        self.branch = branch
        self.is_cloned = False

    def remove_local_repository(self):
        ''' Удаление локального репозитория. Возвращает в случае успеха True,
        иначе False '''
        if (not self.local_path or self.local_path == '/tmp/'):
            return False
        try:
            shutil.rmtree(self.local_path)
            self.is_cloned = False
        except:
            return False
        return True


class GitRepository(Repository):
    """ Класс для работы с git репозиторием """
    def __init__(self, git_url, to_dir='/tmp/', branch='master'):
        super().__init__(git_url, to_dir, branch)

    def clone_url(self):
        ''' Возвращает путь до каталога, куда был клонирован репозиторий
        В случае ошибки возвращает пустую строку '''
        if not self.git_url:
            return ''
        # на всякий случай чистим каталог
        self.remove_local_repository()
        try:
            Repo.clone_from(
                self.git_url, self.local_path, branch=self.branch
            )
            self.is_cloned = True
        except:
            # Чистим за собой
            self.remove_local_repository()
            self.local_path = ''
            self.is_cloned = False
        return self.local_path


class HgRepository(Repository):
    """ Класс для работы с hg репозиторием """
    def __init__(self, git_url, to_dir='/tmp/', branch='master'):
        super().__init__(git_url, to_dir, branch)

    def clone_url(self):
        ''' заглушка '''
        pass
