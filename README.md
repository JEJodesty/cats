# CATs: Content-Addressable Transformers
![alt_text](images/CATs_chaordic_kernel.jpeg)

## Description:
**Content-Addressable Transformers** (**CATs**) is a unified Data Service Collaboration framework for organizations 
implemented as an edge-computing service that establish a Data Mesh as a scalable self-serviced Data Platform of 
Data Products with Data Provenance. CATs connect collaborators between organizations on a Data Mesh via the 
Content-Addressed Storage(CAS) of interoperable and scalable data processing to enable Data Provenance. CAT data 
processing workloads (CATs) are deployable as parallelized and distributed processes at horizontal & vertical scale to 
support scalable (big) data processing microservices with Scientific Computing capabilities. CATs are also integration 
points which enable scaled data processing portability between client-server cloud platforms and mesh (p2p) networks 
with minimal rework or modification.

CATs are submitted as content-addressed Orders of data processes (transformers) which are Invoiced for verification and 
logged as Bills-Of-Materials that serve as Data Provenance records. These records are content-addressed as unique 
identifiers of CAT workloads and their content. CATs content-addresses are also used as URIs that provide a means of 
data transportation. Therefore, the implementation of CATs' as content-addressed data processes establishes and 
self-services a scalable Data Platform as a Data Mesh network of interoperable distributed computing workloads 
deployable on Kubernetes as CATs execution paradigm. 

CATs enables the 
[continuous reification of **Data Initiatives**](https://github.com/DynamicalSystemsGroup/cats?tab=readme-ov-file#continuous-data-initiative-reification) 
by cataloging discoverable, accessible, and re-executable workloads as 
[**Data Service Collaboration**](https://github.com/DynamicalSystemsGroup/cats?tab=readme-ov-file#continuous-data-initiative-reification) 
composable records between organizations. These records provide a reliable and efficient way to manage, share, and 
reference data processes via [**Content-Addressing**](https://en.wikipedia.org/wiki/Content-addressable_storage) Data 
Provenance records.

**Content-Addressing** is a method of uniquely identifying and retrieving data based on its content rather than its 
location or address. CATs provides verifiable data processing and transport on a Mesh network of CATs interconnected by 
Content-Addressing Data Provenance records with [IPFS](https://ipfs.io/) 
[**CIDs**](https://docs.ipfs.io/concepts/content-addressing/) (Content-Identifiers) as content addresses issued by IPFS 
**[client](https://docs.ipfs.io/install/command-line/#official-distributions)** to identify and retrieve inputs, 
transformations, outputs, and infrastructure (as code [IaC]) for verifying transformation accuracy given CIDs.
![alt_text](images/cid_example.jpeg)

### Specification:
CATs' utilizes [Ray](https://www.ray.io/) for interoperable & parallelized distributed computing frameworks deployable 
on **[Kubernetes](https://kubernetes.io/)** for Big Data processing with Scientific Computing. Ray is a unified compute 
framework that enables the development of parallel and distributed applications for scalable data transformation, 
Machine Learning, and AI. Ray provides CATs with interoperable computing frameworks with its 
[ecosystem integrations](https://docs.ray.io/en/latest/ray-overview/ray-libraries.html) such as 
[Apache Spark](https://spark.apache.org/), and [PyTorch](https://pytorch.org/).

Ray is deployed as an execution middleware on Kubernetes. IPFS serves as CATs' Data Mesh's network layer to provide 
parallelized data ingress and egress for IPFS data. This network portability closes the gap between data analysis and 
business operations by connecting the network planes of the cloud service model (SaaS, PaaS, IaaS) with IPFS. CATs 
connect these network planes by enabling the instantiation of FaaS with cloud services in AWS, GCP, Azure, etc. on a 
**Data Mesh** network of CATs. IPFS enables this connection as p2p distributed-computing job submission in addition to 
the client-server job submission provided by Ray.
![alt_text](images/simple_CAT2b.jpeg)

### Get Started!:
0. **Install [Dependencies](./docs/DEPS.md)**
1. **Install CATs:**
    ```bash
    git clone git@github.com:DynamicalSystemsGroup/cats.git
    cd cats
    python -m venv venv # Create Virtual Environment
    source venv/bin/activate # Activate Virtual Environment
    python -m pip install --upgrade pip
    pip install dist/*.whl
    ```
2. **Demo:** [**Establish a CAT Mesh**](./docs/DEMO.md)
3. **Test:** [**CAT Mesh Verification**](./docs/TEST.md)

### [Contribute!](docs/CONTRIBUTING.md)

### Continuous Data Initiative Reification:
**Data Initiatives** will be naturally reified as a result of **Data Service Collaboration** on CATs. CATs will be 
compiled and executed as interconnecting services on a Data Mesh that grows naturally when organizations communicate 
CATs provenance records within feedback loops of Data Initiatives.
![alt_text](images/CATs_bom_ag.jpeg)

### CATs' Architectural Quantum:
Organizations and collaborators participating will employ CATs for rapid ratification of service agreements within 
collaborative feedback loops of [**Data Initiatives**](https://github.com/DynamicalSystemsGroup/cats?tab=readme-ov-file#continuous-data-initiative). 
CATs' apply an **Architectural Quantum** Domain-Driven Design principle described in 
[**Data Mesh of Data Products**](https://martinfowler.com/articles/data-mesh-principles.html) to reify Data Initiatives.
(* [**Design Description**](docs/DESIGN.md))

The Action Plane is the Analytical Data Processing interface. The Action Plane orchestrates and supervises 
how virtual resources owned by the Data Product should be managed, routed, and processed and is stored “offmesh” 
(“offline”). It supervises the exchange of data between sub-Process components within the Data sub-Plane (Process) in 
adherence to Data Contracting Standards of organizations participating in a Data Mesh.
![alt_text](images/CATkernel.jpeg)

#### Quantum Architecture Description as a [Minimal Federated Operating Model](https://www.starburst.io/blog/data-mesh-book-bulletin-principle-of-federated-computational-governance/)
* **Function** is a FaaS for scalable Data Processing and analytics executed as CAT **Processes**. Functions (FaaS) are deployed 
on Structure (PaaS) to execute Processes orchestrated by InfraFunctions (FaaS) 
  * **Processes** are **Functional Data Processors** executable by InfraFunctions (FaaS) deployed on Structure (PaaS), and 
  contextualized with pre and post processed data by InfraFunctions (FaaS). Processes (FaaS) are executed with and made 
  orchestratable by InfraFunctions (FaaS) to support the following use-cases
    * The CAT Order is updated with the inclusion of resulting mutated Functions (FaaS) for execution processed by CATs 
    Factory Client.
  * **InfraFunction (FaaS) is a Data Processing orchestrator** that employs a CAR for the configurable execution of scalable 
  **Process**ing operated by the Plant (SaaS)
    * The CAT Order is updated in alignment CATs Architectural Quantum’s Functionality. This Order will include the 
    resulting updated of Structure (PaaS) with respect to the updated Plant (SaaS) and an updated Function (FaaS) with 
    updated Ingress and Egress subProcesses (FaaS)
* **Structure** (**PaaS** as **IaC**) provisions and maintains the Plant (SaaS) as Function’s (FaaS) scalable execution environment. 
  * The **Plant (SaaS)** is **InfraStructure’s (IaaS)** dynamically scaled execution environment of **Function (FaaS)** 
  as an IaC plugin(s)
    * The web application codebase is Content Addressed within CAT Orders as Data Contract metadata for Order registration. 
  * **InfraStructure (IaaS)** supports the provisioning of dynamically scaled infrastructure for maintaining a Plant (SaaS).
    * The CAT Order is updated in alignment with event-driven functionality and operations with the resulting mutation 
    of Structure (PaaS).

### CATs' Data Provenance Record:
**BOM (Bill of Materials)** are CATs' Content-Addressed Data Provenance record for verifiable data processing and 
transport on a Mesh network of CATs. BOMs are used as CAT’ input & output that contain CATs’ means of data processing.
* BOMs employ CIDs for location-agnostic retrieval based on its content as well as processes and 
[Data Verification](https://en.wikipedia.org/wiki/Data_verification). BOM CIDs can be used to verify the means of processing 
data (input, transformation / process, output, infrastructure-as-code (IaC)) they can also make CATs resilient by 
enabling re-execution via retrieval. CATs certifies the accuracy of data processing on data products and pipelines by 
enabling maintenance and reporting of 
[data and process lineage & provenance](https://bi-insider.com/posts/data-lineage-and-data-provenance/) as chains of 
evidence using CIDs.
![alt_text](images/CATs_bom_activity.jpeg)
* CAT Mesh is composed by CATs executing BOMs.
![alt_text](images/CATs_bom_connect.jpeg)

### CAT Mesh: CATs Data Mesh platform with Data Provenance
**CAT Mesh** is a self-serviced Data Mesh platform with Data Provenance. **CAT Nodes** are CAT Mesh peers that enable 
workloads to be portable between client-server cloud platforms and p2p mesh network with minimal rework or modification.

Multi-disciplinary and cross-functional teams can use CAT Nodes to verify and scale distributed computing workloads. 
Workloads (CATs) executed by CAT Nodes interface cloud service model (SaaS, PaaS, IaaS) offered by providers such as 
AWS, GCP, Azure, etc. on a Mesh Network interconnected by IPFS. 

CAT Nodes are **Data Products** - peer-nodes on a mesh network that encapsulate components (*) to function as a service 
providing access to a domain's analytical data as a product; * code, data & metadata, and infrastructure.

**In the following image:** 
* Large ovals in the image above represent **Data Products** servicing each other with Data
* "O" ovals are Operational Data web service endpoints
* "D" ovals are Analytical Data web service endpoints
* Source: [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) - Zhamak 
Dehghani, et al.
![alt_text](images/data_product_domain.jpeg)

## Key Concepts:
* **[Data Verification](https://en.wikipedia.org/wiki/Data_verification)** - a process for which data is checked for 
accuracy and inconsistencies before processed
* **[Data Provenance](https://bi-insider.com/posts/data-lineage-and-data-provenance/)** - a means of proving data 
lineage using historical records that provide the means 
of pipeline re-execution and **[data validation](https://en.wikipedia.org/wiki/Data_validation)**
* **[Data Lineage](https://bi-insider.com/posts/data-lineage-and-data-provenance/)** - reporting of data lifecyle from 
source to destination
* **[Distributed Computing](https://en.wikipedia.org/wiki/Distributed_computing)** - typically the concurrent and/or 
parallel execution of job tasks distributed to networked computers processing data
* **[Bill of Materials (BOM)](https://en.wikipedia.org/wiki/Bill_of_materials)** - an extensive list of raw materials,
components, and instructions required to construct, manufacture, or repair a product or service

### Image Citations:
* **["Illustrated CAT"](https://github.com/DynamicalSystemsGroup/cats#illustrated-cat)**
  * [Python logo](https://tse4.mm.bing.net/th?id=OIP.ubux1yLT726_fVc3A7WSXgHaHa&pid=Api)
  * [SQL logo](https://cdn3.iconfinder.com/data/icons/dompicon-glyph-file-format-2/256/file-sql-format-type-128.png)
  * [Terraform logo](https://tse2.mm.bing.net/th?id=OIP.1gAEVon2RF5oko4iWCfftgHaHO&pid=Api)
  * [IPFS logo](https://tse1.mm.bing.net/th?id=OIP.BRyW5Tdm5_6VQxCsGr_sQAHaHa&pid=Api)
  * [cat image](https://tse1.mm.bing.net/th?id=OIP.xS_itpeyTImMcrcQ_YNsfQHaIu&pid=Api)
  * [ray.io logo](https://open-datastudio.io/_images/ray-logo.png)
  
## Acknowledgments

CATs was developed by the [Dynamical Systems Group (DSG)](https://github.com/DynamicalSystemsGroup) team.

**Key contributions:**
- **Network Architecture & Verified Information Exchange:** 
  - [Michael Zargham (mzargham)](https://github.com/mzargham) 
  - [David Sisson](https://github.com/davidfsol5)
- **Lead Solutions Architect & Developer / Distributed Systems Engineer** 
  - [Joshua E. Jodesty](https://github.com/JEJodesty)
- **Testing:** Danilo
