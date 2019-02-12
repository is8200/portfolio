import docker

class DockerContainer:
    def __init__(self) :
        #컨테이너 정보 수정
        self.extraHosts = {'sparkclient': '172.18.0.2' \
                , 'sparknamenode' : '172.18.0.3' \
                , 'sparkdatanode' : '172.18.0.4' \
                , 'sparkresourcemanager' : '172.18.0.6' \
                , 'sparknodemanager' : '172.18.0.5' }
        
        self.containerVolume = {'e:/kiha/sharedDir/cgroup' : {'bind' : '/sys/fs/cgroup', 'mode': 'ro'} \
            ,'e:/kiha/sharedDir/hadoopConf' : {'bind' : '/etc/hadoop/conf', 'mode': 'ro'}}

    def open(self, imageName, containerName, containerVolume, containerIp):
        self.containerName = containerName
        containerAllVolume = self.containerVolume.copy()
        containerAllVolume.update(containerVolume)
        self.containerIp = containerIp
        self.imageName = imageName   
        #print(containerAllVolume)
        #컨테이너 노드 실행
        self.client = docker.from_env()
        container = self.client.containers.run(self.imageName \
            , hostname = self.containerName \
            , domainname = self.containerName \
            , name = self.containerName \
            , cap_add = 'SYS_ADMIN' \
            , detach = True \
            , extra_hosts = self.extraHosts \
            #, network = 'spark-network' \
            , privileged = True \
            , volumes = containerAllVolume)
        self.client.networks.get('spark-network').connect(container, ipv4_address = self.containerIp )
        #print(container.logs())
    def close(self, containerName):
        sContainer = self.client.containers.get(containerName)
        sContainer.stop()
        sContainer.remove()
        
    def exec(self, containerName, commandDocker):
        sContainer = self.client.containers.get(containerName)
        #print(sContainer.logs())
        sLog = sContainer.exec_run(commandDocker)
        print(sLog)