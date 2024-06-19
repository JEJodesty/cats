class Plant:
    def __init__(self, service):
        self.service = service
        self.INPUT_PLANT_HOME = self.service.INPUT_PLANT_HOME
        self.export_tf_data_dir_cmd = f"export TF_DATA_DIR={self.INPUT_PLANT_HOME}"
        print(self.export_tf_data_dir_cmd)
        self.service.executeCMD(self.export_tf_data_dir_cmd, cwd=self.INPUT_PLANT_HOME)


class InfraStructure:
    def __init__(self, service):
        self.service = service
        self.INPUT_PLANT_HOME = self.service.INPUT_PLANT_HOME
        self.initialize()

    def destroy(self):
        print('Destroy Structure!')
        self.service.executeCMD(
            'terraform destroy --auto-approve',
            cwd=self.INPUT_PLANT_HOME
        )
        print()
        print()

    def plan(self):
        print('Plan Structure!')
        self.service.executeCMD(
            'terraform plan',
            cwd=self.INPUT_PLANT_HOME
        )
        print()
        print()

    def initialize(self):
        print('Initialize Structure!')
        self.service.executeCMD(
            'terraform init --upgrade',
            cwd=self.INPUT_PLANT_HOME
        )
        print()
        print()

    def apply(self):
        print('Apply Structure!')
        self.service.executeCMD(
            'terraform apply --auto-approve',
            cwd=self.INPUT_PLANT_HOME
        )
        print()
        print()