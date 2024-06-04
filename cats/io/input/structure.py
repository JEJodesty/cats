class Structure:
    def __init__(self,
        service=None
    ):
        self.service = service
        self.bom_json_cid = self.service.bom_json_cid
        # self.plant: Plant = plant
        # self.infraStructure: Terraform = Terraform(working_dir=cats.CWD)

    def destroy(self):
        print('Destroy Structure!')
        self.service.executeCMD(['terraform', 'destroy', '--auto-approve'], cwd=self.service.CATS_HOME)
        print()
        print()

    def initialize(self):
        print('Initialize Structure!')
        # self.service.executeCMD(['terraform', 'plan'])
        self.service.executeCMD(['terraform', 'init', '--upgrade'], cwd=self.service.CATS_HOME)
        print()
        print()

    def apply(self):
        print('Apply Structure!')
        self.service.executeCMD(['terraform', 'apply', '--auto-approve'], cwd=self.service.CATS_HOME)
        print()
        print()

    def redeploy(self):
        print()
        print()
        print('Deploy Structure!')
        self.destroy()
        self.initialize()
        self.apply()
