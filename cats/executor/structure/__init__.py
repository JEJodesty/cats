class InfraStructure:
    def __init__(self, service):
        self.service = service
        # self.infraStructure: Terraform = Terraform(working_dir=cats.CWD)

    def destroy(self):
        print('Destroy Structure!')
        self.service.executeCMD(['terraform', 'destroy', '--auto-approve'], cwd=self.service.CATS_HOME)
        print()
        print()

    def plan(self):
        print('Plan Structure!')
        self.service.executeCMD(['terraform', 'plan'], cwd=self.service.CATS_HOME)
        print()
        print()

    def initialize(self):
        print('Initialize Structure!')
        self.service.executeCMD(['terraform', 'init', '--upgrade'], cwd=self.service.CATS_HOME)
        print()
        print()

    def apply(self):
        print('Apply Structure!')
        self.service.executeCMD(['terraform', 'apply', '--auto-approve'], cwd=self.service.CATS_HOME)
        print()
        print()