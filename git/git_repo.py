import subprocess


class GitRepo:
    def __init__(self, project_path):
        self.project_path = project_path

    def stash(self):
        git = 'git'
        stash = 'stash'
        save = 'save'
        message = 'Stashed by GITAG'
        output = subprocess.check_output([git, stash, save, message], cwd=self.project_path)
        return not output.find('No local changes to save') != -1

    def stash_pop(self):
        git = 'git'
        stash = 'stash'
        pop = 'pop'
        subprocess.check_call([git, stash, pop], cwd=self.project_path)

    def get_current_branch(self):
        git = 'git'
        rev_parse = 'rev-parse'
        abbrev_ref = '--abbrev-ref'
        head = 'HEAD'
        return subprocess.check_output([git, rev_parse, abbrev_ref, head], cwd=self.project_path).replace('\n', '')

    def checkout_to_branch(self, branch):
        git = 'git'
        checkout = 'checkout'
        subprocess.check_call([git, checkout, branch], cwd=self.project_path)

    def diff_versions(self, branch_1, branch_2):
        git = 'git'
        diff = 'diff'
        numstat = '--numstat'
        return subprocess.check_output([git, diff, numstat, branch_1, branch_2], cwd=self.project_path)
