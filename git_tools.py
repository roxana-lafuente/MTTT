import git, os, shutil
import datetime
import uuid
import sys
from github import Github
from github import BadCredentialsException

def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dirs]:
            os.chmod(dir, mode)
    for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)

class GitWrapper:

    def login_to_Github(self, user,passwd):
        self.user = user
        self.passwd = passwd
        try:
            g = Github(user, passwd)
            for repo in g.get_user().get_repos():
                pass
            return 1
        except BadCredentialsException:
            print "bad"
            return 0

    def ifRepositoryIsNotForkedThenFork(self, repo_owner, repo_to_fork_name):
        wasAlreadyForked = 0
        g = Github(self.user, self.passwd)
        for repo in g.get_user().get_repos():
            if repo.name == repo_to_fork_name:
                wasAlreadyForked = 1

        github_user = g.get_user()
        if not wasAlreadyForked:
            pygithub = g.get_user(repo_owner).get_repo(repo_to_fork_name)
            myfork = github_user.create_fork(pygithub)
        return wasAlreadyForked


    def clone_this(self, username, password,repoURL):
        self.username = username
        self.password = password
        self.repoURL = repoURL
        self.TEMP_DIR = ".temp/"
        self.DIR_NAME = self.TEMP_DIR + str(uuid.uuid4())
        self.REMOTE_URL = "https://" + self.username + ":" + self.password + self.repoURL
        if os.path.isdir(self.TEMP_DIR):
            shutil.rmtree(self.TEMP_DIR)

        os.mkdir(self.TEMP_DIR)
        os.mkdir(self.DIR_NAME)
        '''
        the following line is neccesary since by making temp hidden by adding a point to its DIR_NAME,
        its permissions are changed to READ-ONLY
        '''
        change_permissions_recursive(self.DIR_NAME,0o666)#change to READ-WRITE
        self.clone()

    def get_dir_name(self):
        return self.DIR_NAME

    def clone(self):
        '''
        clones the repo
        '''
        repo = git.Repo.init(self.DIR_NAME)
        origin = repo.create_remote('origin',self.REMOTE_URL)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)
        self.repo = git.Repo('./' + self.DIR_NAME)

    def commit(self, file = "test.txt"):
        '''
        using this instead of commitNpush
        reduces latency since it does not
        exchange information with the cloud
        '''
        self.repo.git.add(file)
        self.repo.git.commit( m= datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

    def push(self):
        '''
        quite self explanatory
        '''
        self.repo.git.push()

    def commitNpush(self, modified_reference):
        '''
        using this guarantees that changes are uploaded.
        Sort of GoogleDocs in the sense that it does not
        let the user continue adding information
        until the current information is saved in the cloud
        '''

        text_file = open(self.DIR_NAME + "/test.txt", "w")
        text_file.write(modified_reference)
        text_file.close()

        self.commit()
        self.repo.git.push()
