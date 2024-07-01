### Week 0 (1/2 - 1/5):
Update readme and refactor 

### Week 1 (1/8 - 1/12): 
* Review Designs within the context of Data Sovereignty;
  * https://en.wikipedia.org/wiki/Data_sovereignty
  * https://www.ibm.com/blog/living-in-a-data-sovereign-world/
  * https://atlan.com/data-sovereignty-requirements/
* Research CLI wrapper alternative to CDKTF 
* Review Database Sharding within the context of Data Products’ data: https://aws.amazon.com/what-is/database-sharding/
* Review Value of data
* Verify CATs’ Project Update: Factory & Executor components; Invoice, Order, Function, Executor, & BOM Block Designs, Structure’s Ray Cluster Deployment  on Kubernetese, BOM Initialization, CAT Node & Node Design

### Week 2 (1/15 - 1/19):
* Research Dynamic Terraform Providers for Plant Deployments
* Verify CATs’ Project Update: Structure Block Design, Data Service Collaboration Diagram, Ray Integration
* Watched Computational Governance Panel
* Review Ray documentation for InfraFunction Hooks
* Research Open Contracting Data Standard with respect to Data Product Teams: https://standard.open-contracting.org/latest/en/

### Week 3 (1/22 - 1/26)
* 1/22: 
  * Updated CATs integration tests and demo
  * Resolved dependency bug
  * Verify CATs’ Project Update: Process Component, Sub-Process Logging, Executor & Function Components
* 1/23: 
  * Updated Documentation and Demo
  * Added License and Packaging for CATs
  * Verify CATs’ Project Update: s3 & CoD Integration
* 1/24: 
  * Updated Documentation & Refactor
  * CATs Data Verification
  * Verify CATs’ Project Update: Updating Order Structure, Node, Service & Structure Components
* 1/25 - 1/26: 
  * Updated Documentation & Refactor
  * Update Factory
  * Reviewed Novo Nordisk Data Mesh Platform discussion
  * Verify CATs’ Project Update: CATs s3 cache, BOM ERD

### Week 4 (1/29 - 2/2): 
* Included Ubuntu 20.04 Installation Update
* Refactored CATs
* Researched CAT cache access management
* Research Economic Adapters for CATs
* Research multilevel linked-list for CATs’ subgraph


### Week 5 (1/5 – 1/9): 
* Research bidirectional mapping supports multilevel linked-list for CATs’ subgraph
* Consider Transducers for CAT MIMO
* Updated PR Template
* Review Model-Driven Engineering: https://en.wikipedia.org/wiki/Model-driven_engineering

### Week 6 (2/12 - 2/16):
* 2/12: Drafted CATs capabilities in GitHub Project and reviewed Activity Artifact Policy
* 2/13: Reviewed implementation examples of Data Contracts
* 2/14 - 2/15: 
  * Reviewed Data Mesh Roundtable Discussions about Data Contracts and “Agile” Data Products
  * Attended Protocol Labs project updates
* 2/16: Research System Architecture layers and wrote notes as Data Contract Article for CATs

Data Mesh Resources:
* “Inside a Data Contract”: https://www.youtube.com/watch?v=ye4geXMuJKs
* “Agile in Data”: https://www.youtube.com/watch?v=XnstATam0jM
* Data Contract Articles: https://www.datamesh-architecture.com/#data-contract

Data Contract Implementation Examples:
* https://blog.det.life/data-contracts-a-guide-to-implementation-86cf9b032065
* https://levelup.gitconnected.com/create-a-web-scraping-pipeline-with-python-using-data-contracts-281a30440442
* https://docs.soda.io/soda/data-contracts.html

System Architecture:
* https://blog.jgriffiths.org/systems-architecture-conceptual-logical-and-physical/

What does a CATs data contract do?

Data Contract is a Service agreement between producer and consumer with attribute dependencies for downstream Data Product evolution with dedicated lineage. A data contracts can provide tools for collaboration on data requirements as product promises within a shared context that inform policies for contract mutation along side Data Product releases.

A Data Contract’s Product Promises are what the data product owners expect from its data consumer up to the latest block of information. These promises may include data quality, data usage terms and conditions, schema, service-objectives, billing, etc. Data Contract policy mutation cascaded downstream as bilateral lateral agreements that “forks” lineage as a new Data Product version. For Example, the consumer takes the risk of violating privacy. Data Producers create Data Contracts on Organization and Business Terms. The consumer of the Data Contract enforces Governance policies. The producer of the Data Contract owns the Data Product if the organization doesn't have a Governance body. 

Governance policies are discussed between data producers and consumers to agree upon data producer requirements. These discussions should culminate into an amenable data structure / dataset. Structured data is conducive for pre-exsisting policies and less discussion. Less structured data will need more discussion and policy feedback loops. We need a Minimal Viable Data Contract that includes what is necessary for an organization to govern with the means of supporting policy feedback loops in a way that guides discussion in a way that balances the prioritization of outcomes and methodologies.

Interdependent data domains have sub-domains with identifiers for generating Data Products. CAT Nodes will generate and execute Virtual Data Products composed as Data Contracts that enforce Data Provenance using Bills of Materials (BOMs). BOMs are CATs' Content-Addressed Data Provenance record for verifiable data processing and transport on a Mesh network of CAT Nodes. Data Contracts will contain a BOMs lineages and act as block headers for Content-Addressed Transformers (CATs) instances. Data Products are mutated during policy feedback loops informed collaborators communicating their understanding of knowledge domains. Collaborators will identify knowledge sub-domains with references and will access sub-domains using Content-Addresses. Access is federated via knowledge domain hierarchies in abstractions that enable collaborators to participate in governance cycles by leveraging their understanding of knowledge.

### Week 7 (2/19 - 2/23):
* 2/19 - 2/21: Contextualize value of BOM within the context of Data as a Product that contains Data Contracts
* 2/22 - 2/23: Updated Readme informed by examples of Data Assets within the context of Machine-Readable Cataloging

Resources:
* https://www.loc.gov/marc/umb/um01to06.html
* https://docs.informatica.com/data-engineering/data-engineering-quality/10-2-1/business-glossary-guide/glossary-content-management/business-term-links/data-asset.html

What is a Content-Addressed Data Asset (CADA)?

CATs Data Products will consist of Data Contracts with provenance as executable BOMs lineages and act as block headers for Content-Addressed Transformers (CATs) instances that contain Data Assets. BOMs are CATs' Content-Addressed Data Provenance record for verifiable data processing and transport on a Mesh network of CAT Nodes that can contain Data Assets. A data asset may be a system or application output” (dataset) that holds value for an organization or individual that is accessible. Data Assets’ value can derive from the data's potential for generating insights, informing decision-making, contributing to product development, enhancing operational efficiency, or creating economic benefits through its sale or exchange. 

CATs' Content-Addressed Data Assets are processed, sold / exchanged / published on CAT’s Data Mesh via CAT Nodes subsumed by downstream CATs’ Data Products. Data Assets consist of the following:
* **Data Domains** - "A predefined or user-defined Model repository object that represents the functional meaning of an" attribute "based on column data or column name such as" account identification.
* **Data Objects** - Content-Addresses of data sources used to extract metadata for analysis.

### Week 8 (2/26 - 3/1):

* 2/26: Researched Digital Asset Management related Data Contracts and Data Mesh Registry & considered a Rule Asset being used for Network Policies in addition to Attribute Quality 
* 2/27: Considered Data & Rule Assets for Data Mesh Registry Artifact Schema
  * https://towardsdatascience.com/the-data-mesh-registry-a-window-into-your-data-mesh-20dece35e05a 
  * https://docs.informatica.com/data-engineering/data-engineering-quality/10-2-1/business-glossary-guide/glossary-content-management/business-term-links/data-asset.html
  * https://docs.informatica.com/data-engineering/data-engineering-quality/10-2-1/business-glossary-guide/glossary-content-management/business-term-links/rule-asset.html
* 2/28: Verify CATs Executing FaaS on PaaS
  * https://www.ibm.com/topics/faas
  * https://www.ibm.com/topics/iaas-paas-saas
* 2/29: Review Domain-Oriented Ownership with respect to Conway's law
  * https://www.starburst.io/blog/data-mesh-book-bulletin-principle-of-domain-ownership/
  * https://developer.confluent.io/courses/data-mesh/data-ownership/
  * https://en.wikipedia.org/wiki/Conway%27s_law
* 3/1: Review Data Column Lineage value to in establishing Domain-Oriented Ownership in CATs Invoice in a way that makes BOM’s searchable and discoverable

What makes CATs Governable by including BOMs within Data Product’s Data Contracts?

CATs are governable and support multi-disciplinary collaboration of data processing because CATs Architectural Quantum is an abstract governance model enforced within CATs’ Bills-Of-Materials (BOMs) for which knowledge domains are represented as meta-data of data provenance records to support domain ownership. 

BOMs are unique identifiers that provide the means of data production (assembly) and transportation as reproducible lineage contextualised by knowledge domains for federated governance. BOMs consist of Data Product service Orders of data processing that are Invoiced as fulfillments of service agreements specified by Data Product’s Data Contracts

Federated Governance is enabled by BOMs due the following. The domain specific data provenance BOMs establish the legitimacy of network policy changes suggested by Fractional Stewards of Data Products by enabling them to identify data quality issues at their source on a self-serviced Data Platform of many Data Products. 

CATs enables Fractional Stewards to do this because historical data production is contextualised and reproducible within the scope of their knowledge domains by design during development and production as a requirement of a service Order. CATs data processes submitted by their service Orders are Invoiced to fulfil agreements within Data Products’ Data Contracts.

A Data Contract is a Service agreement between producer and consumer with attribute dependencies for downstream Data Product evolution with dedicated lineage. Governance policy discussions between data producers and consumers in policy feedback loops about data production requirements should balance the prioritization of outcomes and methodologies should culminate into an amenable data structure / dataset.

### Week 9 (3/4 - 3/8):
* 3/4: Contextualize “Data as an asset” with CATs Architecture
  * https://atlan.com/data-as-an-asset/
* 3/5: Contextualize Data sovereignty with “Data as an asset” for CATs Data Mesh
  * https://www.nnlm.gov/guides/data-glossary/data-sovereignty#:~:text=Definition,storage%2C%20and%20interpretation%20of%20data.
* 3/6: Contextually map Data Contract initialization roles to cross-functional Operational Model for Data Products
  * https://standard.open-contracting.org/latest/en/guidance/design/#build-your-team
* 3/7: Contextually map "Fractional Ownership" of "Decentralized Data Objects" ("DDOs" / "Data Assets") to "Data as an asset" and Data Partioning / Sharding
  * https://docs.oceanprotocol.com/developers/fractional-ownership 
  * https://docs.oceanprotocol.com/developers/ddo-specification
  * https://en.wikipedia.org/wiki/Partition_(database)
  * https://en.wikipedia.org/wiki/Shard_(database_architecture)
* 3/8: Contextualize Ocean Protocol & CATs Architecture with prosumption
  * https://docs.oceanprotocol.com/developers/architecture 
  * https://en.wikipedia.org/wiki/Prosumer

“Data as an asset” enables the consumption, production, [prosumption](https://en.wikipedia.org/wiki/Prosumer) of Data Assets on CATs Data Mesh

“Data as an asset” [0.](https://atlan.com/data-as-an-asset/) conceptually emphasizes recognizing and treating data as a strategic investment organizations can leverage to deliver future economic benefits by enabling the consumption, production, prosumption of ones own data as an asset. Prosumption is the consumption and production of value, "either for self-consumption or consumption by others, and can receive implicit or explicit incentives from organizations involved in the exchange." [1.](https://doi.org/10.1108/JOSM-05-2020-0155)

The availability of high-quality and domain-specified Data Assets enables Data Products on inter-connected CAT Nodes on CATs Data Mesh to facilitate cross-functional asset utilization within Data Initiatives in a way that support Data Sovereignty. "Data sovereignty refers to a group or individual’s right to control and maintain their own data, which includes the collection, storage, and interpretation of data." [2.](https://www.nnlm.gov/guides/data-glossary/data-sovereignty#:~:text=Definition,storage%2C%20and%20interpretation%20of%20data.)

Registering and cataloging CATs can accelerate innovative Data Product creation and facilitate Data Sovereignty in Data Initiatives that discover and utilize “Data as an asset”. Data Products use and operate CAT Nodes to produce, register, and catalog “Data as an asset” as searchable and discoverable Data Assets by Data Products on CATs Data Mesh. CATs Data Assets enhances strategic, operational, and analysis informed decision-making by using BOMs as feedback loop mechanisms across domains in a way that suits specific collaborative contexts across organizations.

Resources:
* https://www.youtube.com/watch?v=uv52swYfStU&t=6s
* https://www.youtube.com/watch?v=pbBGciy8ZbM

### Week 10 (3/11 - 3/15):

* 3/11: Review ocean Data NFTs and Datatokens and relate Hexagonal architecture to Data Contract SLAs
  * https://docs.oceanprotocol.com/developers/contracts/datanft-and-datatoken
  * https://en.wikipedia.org/wiki/Non-fungible_token#:~:text=A%20non%2Dfungible%20token%20(NFT,to%20be%20sold%20and%20traded.
  * https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
  * https://blog.thepete.net/blog/2020/09/25/service-templates-service-chassis/
* 3/12
  * Review Bidirectional Mapping libraries for Data Mesh BOM graph for cataloged representation
    * example: https://github.com/jab/bidict
  * Review Custom Terraform Provider software that enables providers to be written in any language for CATs Plant
    * https://github.com/birchb1024/terraform-provider-universe
    * https://github.com/beelit94/python-terraform
  * Review Model-Based System Engineering relate it to knowledge organization infrastructure
    * https://medium.com/block-science/what-is-blockscience-6e3c9ac21637
  * https://medium.com/block-science/knowledge-networks-and-the-politics-of-protocols-af81ad0fa2d4
* 3/13 - 3/15
  * Review 4 kinds of data moats within the context of data’s strategic value as a “data asset”
    * https://towardsdatascience.com/the-4-kinds-of-data-moats-that-your-company-can-build-c68f691b435c
  * Review Model-driven architecture approaches for CATs Architectural Quantum
    * https://en.wikipedia.org/wiki/Model-driven_architecture
  * Review ocean.py for integration into CATs’ ingress and egress
    * https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/custody-light-flow.md
  * Review “Commons-based peer production” for CAT Node
    * https://en.wikipedia.org/wiki/Commons-based_peer_production
  * Updated CATs architecture, readme, and interactive logs

### Week 11 (3/18 - 3/22):

* 3/18 - 3/20: Contextualize data contract creation team' role responsibilities into modern roles
* 3/21 - 3/22: 
  * Contextualize modern data contract creation team' role responsibilities into CATs Control and Action planes for an operational model for the placement of Data Stewardship responsibilities
  * Communicate the value of Data Contract inclusion in BOM bellow.

Why should Data Contracts be included in CATs' BOMs for Data Product development on a Data Mesh?

Data Product(s) CATs are executed by Data Contract deployments with Data Provenance by Ordering CATs that are Invoiced within Bills of Materials (BOMs). BOMs are CATs' Content-Addressed Data Provenance record for verifiable data processing and transport on CAT Mesh. Data Contracts will contain BOM lineages and act as headers for Content-Addressed Transformer instances (CATs). Their inclusion of BOMs are necessary for organizations to rapidly mutate Data Products alongside discussions that affect product outcomes and development methodologies. Data Products are mutated during stakeholder discussions about Data Contracts with respect to network policy / protocol. These discussions continuously inform multi-lateral Data Product agreements between stakeholders and collaborators that produce and consume data using BOMs as feedback loop mechanisms for (re)submitting CAT Orders. These discussions should also culminate into a CAT Order of amenable data structures / datasets for which processing is Invoiced within BOMs. Collaborators can participate in data provenance supported product development by Content-Addressing Data as an Asset.

### Week 12 (3/25 - 3/29):

* 3/25 - 3/27: 
  * Review Bitol's Data Contract examples
    * https://bitol.io/
    * https://github.com/bitol-io/open-data-contract-standard
    * https://github.com/bitol-io/open-data-contract-standard/blob/main/examples/README.md
  * Review Data Contract Implementation Guide for CATs
    * https://blog.det.life/data-contracts-a-guide-to-implementation-86cf9b032065
  * Review Wayfair's differentiation of Data Mesh design lean personas: Data Producer, Data Consumers, and Data Engineer
    * https://www.starburst.io/blog/persona-driven-data-mesh-design/
  * Contextualize  IBMs Knowledge Catalog as a DataOps tool in consideration of KMS and CAT-aloging
    * https://www.ibm.com/products/knowledge-catalog
  * Review Statistical Process Control to contextualize the inclusion of https://www.soda.io/
  * Research data product life cycle to contextualize Data Product Manager, Data Steward, and Data Engineer
    * https://www.starburst.io/blog/data-product-lifecycle/
* 3/28 - 3/29: 
  * Contextualize a Federated Governance Model within Federated Computational Governance
    * https://www.starburst.io/blog/data-mesh-book-bulletin-principle-of-federated-computational-governance/
  * Research types of Data Valuation to avoid confirmation bias
    * https://hyperight.com/how-to-monetise-your-data-to-fuel-growth-in-your-business-chat-with-bill-schmarzo/
  * Contextualize Event-Driven programming for CAT Plant and Dataflow programming for CATs Process and InfrFunction
    * https://en.wikipedia.org/wiki/Event-driven_programming
    * https://en.wikipedia.org/wiki/Dataflow_programming

### Week 13 (4/1 - 4/5):
* 4/1 - 4/3:
  * Research "Stewardship Fractalization" and System Architecture facilitating it and relate it to Data Stewardship
    * https://stewardship-fractalization.gitbook.io/project-planning
    * https://stewardship-fractalization.gitbook.io/project-planning/system-architecture-design
  * Consider Dynamic Prompt engineering using Generative AI via an LLM for contextualization of CAT Actions that fulfill Data Contracts. These actions are initially contextualized with CATs Architectural Quantum.
    * https://en.wikipedia.org/wiki/Prompt_engineering
    * https://stewardship-fractalization.gitbook.io/project-planning/generative-ai-chatgpt-claudeai
    * https://en.wikipedia.org/wiki/Generative_artificial_intelligence
    * https://en.wikipedia.org/wiki/Large_language_model
* 4/4 - 4/5:
  * Distinguish between Quantitative and Qualitative design drivers for end-user and data product consumer contextualization
    * https://designlab.com/blog/what-is-data-driven-design#types
  * Consider a Streaming Data Integration for Stewardship lineage views and metadata management
  * Consider each CAT Factory Client a Stream Broker as a Consumer and Producer (https://www.scaler.com/topics/kafka-broker/)
  * Consider "IoT Edge-Application Management" for "IoT Analytics"
    * https://docs.aws.amazon.com/iotanalytics/latest/userguide/welcome.html
  * Consider a language like SISAL for stream dataflow composition
    * http://www2.cmp.uea.ac.uk/~jrwg/Sisal/01.Introduction.html
* Review updated CoD Architecture
  * https://docs.bacalhau.org/getting-started/architecture/

### Week 14 (4/8 - 4/12):
* Research how Analysts supports domain-oriented ownership in consideration of data procurement
  * https://www.starburst.io/blog/data-mesh-and-starburst-domain-oriented-ownership-architecture/
* Research "telemetry data pipelines" from starburst.io to contextualize a “telemetry-catalog” in "data lakehouse" as a flatfile store
  * https://www.starburst.io/blog/how-starbursts-data-engineering-team-builds-resilient-telemetry-data-pipelines/
* Consider Data Engineering pain points to split and contextualize Data Engineering within CATs Action & Control Planes
  * https://www.starburst.io/blog/future-data-engineering/
  * https://www.starburst.io/blog/data-engineering-challenges/
* Distinguish the difference between Data Lakes and Data Federation for the implementation of a data lake solution
  * https://www.starburst.io/data-glossary/data-federation/
* Research GPT to communicate a Federated Governance Model designed to be a GPT
  * https://en.wikipedia.org/wiki/Generative_pre-trained_transformer

### Week 15 (4/15 - 4/19):
* 4/15: 
  * Contextualize LLMs and Generative AI for Fractional Data Stewardship
    * https://stewardship-fractalization.gitbook.io/project-planning/generative-ai-chatgpt-claudeai
  * Reduce scope of Data Product with Stewarship Fractionaliztion dApp steps
    * https://stewardship-fractalization.gitbook.io/project-planning/build-stewardship-fractalization-dapp-on-blockchain
  * Note Dataflow Programming for CAT
    * https://en.wikipedia.org/wiki/Dataflow_programming
  * Note Data Flow Architecture for project definition
    * https://en.wikipedia.org/wiki/Dataflow_architecture
  * Note Statistical process control (SPC) (as user responsibility)
    * https://en.wikipedia.org/wiki/Statistical_process_control
* 4/16-18:
  * Apply Manufacturing Production to BOM design with respect to an Engineering & Manufacturing BOM types
    * https://www.investopedia.com/terms/m/manufacturing-production.asp
    * https://www.investopedia.com/terms/b/bill-of-materials.asp#toc-types-of-bills-of-materials
  * Contextualize CAT orders with a Transfer (Network) Function
    * https://en.wikipedia.org/wiki/Transfer_function
  * Contextually lift Mesh partnership with Model-Based Institution Design (MBID) and relate to Model-Based System Engineering in preperation to include Computer-Aided Governance in CATs3
    * https://medium.com/block-science/model-based-institutional-design-3939b4f0137a
  * Research LangGraph for CAT Mesh reification
    * https://www.langchain.com/
    * https://github.com/langchain-ai/langgraph/tree/main
    * https://python.langchain.com/docs/langgraph/
  * Note different types of SBOMs for each CAT Arch Quantum SubComponents
    * https://github.com/openclarity/kubeclarity
    * https://github.com/anchore/syft
    * https://github.com/ksoclabs/kbom?tab=readme-ov-file
    * https://github.com/kubernetes-sigs/bom
    

### Week 16 (4/22 - 4/26):
* Consider Multi-Agent Conversation for row-wise business function
  * https://arxiv.org/abs/2308.08155
  * https://github.com/langchain-ai/langgraph/blob/main/examples/multi_agent/multi-agent-collaboration.ipynb
  * Consider Pro-curation for on-boarding information onto CAT Mesh reflective of Prosumer
    * https://www.merriam-webster.com/dictionary/procurator
* Research integrating langgraph `tool_node` into CAR (Content-Addressable Router)
  * https://github.com/langchain-ai/langgraph/blob/de9c0786f54db47ae525e49ffb305fbd00462011/langgraph/prebuilt/tool_node.py#L49
* Research integrating langgraph `tool_executor` into CATs' Executor
  * https://github.com/langchain-ai/langgraph/blob/de9c0786f54db47ae525e49ffb305fbd00462011/langgraph/prebuilt/tool_executor.py
* Review LangChain Agents for Network Governance Reification graph state tracking
  * https://github.com/langchain-ai/langgraph/blob/main/examples/agent_executor/force-calling-a-tool-first.ipynb
* Review "Knowledge Networks and the Politics of Protocols" within the context of Roles
  * https://blog.block.science/knowledge-networks-and-the-politics-of-protocols/ 
  * https://github.com/mzargham/RolePlayer/tree/main
  * https://github.com/mzargham/RolePlayer/blob/main/roleplay_test1.ipynb
* Review "Engineering for Legitimacy"
  * https://blog.block.science/engineering-for-legitimacy/

### Week 17 (4/29 - 5/3):
* Review Scaled and Leveled Stewardship
  * https://stewardship-fractalization.gitbook.io/project-planning/generative-ai-chatgpt-claudeai
* Review contextualization of responsibilities based on Prompt Engineering Questions & general responsibilities of "Fractional Stewards"
  * https://stewardship-fractalization.gitbook.io/project-planning/user-stories
* Review Project Roadmap for Stewardship Fractalization in consideration for CAT Team Dynamics
  * https://stewardship-fractalization.gitbook.io/project-planning/project-roadmap
* Review Fractional Stewardship MVP approach in consideration to publishing a Policy development in Steward profile to Agent Nodes in LangGraph. These Policies are front loaded as "algorithmic suggestions"
  * https://stewardship-fractalization.gitbook.io/project-planning/mvps
* Note Abstract User Stories as application references
  * https://stewardship-fractalization.gitbook.io/project-planning/user-stories
* Review "DAO Governance Model" for comparison to Federated Computational Governance Model
  * https://stewardship-fractalization.gitbook.io/project-planning/tokens-and-smart-contract-designs
* Consider Marketing Steward using Prompt Engineering / partial input being a "Comparison Table/Matrix summarizing different Stewardship Organization/Solutions missions/purposes, designs and features"
  * https://stewardship-fractalization.gitbook.io/project-planning/projects-product-market-fit-analysis

### Week 18 (5/6 - 5/10):
* Removing s3 cache from CATs and replace with local storage solution

### Week 18 (5/13 - 5/17):
* Removed s3 cache from CATs and replaced with local storage solution
* Research adaptive Retrieval Augmented Generation (aRAG)
  * https://vercel.com/guides/retrieval-augmented-generation
  * https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/
* Reviewed KMS-identity for integration into CATs
  * https://github.com/BlockScience/kms-identity
* Read "A Language for Studying Knowledge Networks: The Ethnography of LLMs"
  * https://kelsienabben.substack.com/p/a-language-for-studying-knowledge?utm_source=post-email-title&publication_id=198759&post_id=144672529&utm_campaign=email-post-title&isFreemail=true&r=23p95&triedRedirect=true&utm_medium=email

### Week 19 (5/19 - 5/24):
* The Plant is a Transfer Function that accepts an Order as Input and produces and Output with by executing Function (Process) with Executor (Actuator) that executes a Process(es). The Plant exposes the control variable (u(t)) for Control Feedback Loop and the Function (Process) produces the process variable (y(t)). The Process Variable is the Statistical Process Control of CATs Dataset I/O (Ingress/Egress)
  * https://en.wikipedia.org/wiki/Plant_(control_theory)
  * https://en.wikipedia.org/wiki/Actuator
  * https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller
  * https://en.wikipedia.org/wiki/Process_variable
* Docker can be executed within an Alpine Linux Docker container ["Docker in Docker" (DinD)] for upcoming cadCAD's nested Block executions as a summation of the control variable (u(t)) that configure CATs Data Product and the summation of the process variable (y(t))
  * https://www.alpinelinux.org/about/
  * https://en.wikipedia.org/wiki/Process_variable
* Note: "Integral windup particularly occurs as a limitation of physical systems, compared with ideal systems, due to the ideal output being physically impossible (process saturation: the output of the process being limited at the top or bottom of its scale, making the error constant)."
* Concern: "Integral windup particularly occurs as a limitation of physical systems, compared with ideal systems, due to the ideal output being physically impossible (process [saturation](https://en.wiktionary.org/wiki/saturation): the output of the process being limited at the top or bottom of its scale, making the error constant)."
  * https://en.wikipedia.org/wiki/Integral_windup
  * Alleviated by "A CAT at its core is a unit of computational work specified by the triplet 1) what the input is, 
    2) what does the computation, and 3) what the output is.  Controllers require feedback, which is currently 
    outside of the scope of a single cat. Any cyclic orchestration must be external to CATs." - BlockScience
* Alpine Linux Docker can be the execution paradigm of cadCAD and CATs Plant because they can run as Docker inside Docker "DinD” to and functionally map cadCAD multi-dimensional blocks to CAT Functions

### Week 20 (5/27 - 5/31):
* Review RAG stewardship fictionalization context
  * https://stewardship-fractalization.gitbook.io/project-planning/workshop-3-chatgpt-with-rag-retrieval-augmented-generation
* Review Software Governance with respect to fractional stewardship
  * https://standard.open-contracting.org/latest/en/governance/
* Consider a Stewardship Profile that maps to agents within a Multi-agent system
  * [Multi-agent systems](https://en.wikipedia.org/wiki/Multi-agent_system)
* Consider roles as Architectural Responsibilities with respect to [RolePlayer](https://github.com/mzargham/RolePlayer)
* Review Docker workload on-boarding for cat Refactor
  * https://docs.bacalhau.org/setting-up/workload-onboarding/container/docker-workload-onboarding
* Cosider homestar (Everywhere Computer network) for IPVM inclusion for "resilience, certainty or portability"
  * https://github.com/ipvm-wg/homestar/
  * https://fission.codes/ecosystem/ipvm/
  * https://everywhere.computer/
  * https://docs.ipfs.tech/concepts/cod/#bacalhau

### Week 21 (6/3 - 5/7):
* Updated Bacalhau Node and refactor for CoD interoperability for CATs v3
* Exposed ingress and egress to action plane via Process with a interoperable integration point for CATs v3

### Week 22 (6/10 - 6/14):
* Included data product disciplines to CATs Architectural Quantum for CATs v3
* Implement InfraStructure Sub Component separately

### Week 23 (6/17 - 6/26):
* IPFS daemon initiated by CAT Node
* partially implement function for applying sbom
* Refactor infrafunction composes Processor & Plant and Infrstructure
* Installed KMS locally for cat/rid Integration

### Week 24 (6/24 - 6/28):
* bring your own cache otherwise it is local (bg: Expanso introduces breaking changes to bacalhau without stable release)

**What is the Architectural purpose of CATs as a Function a.k.a. the ACG [Monad](https://en.wikipedia.org/wiki/Monad_(functional_programming))?**

* **Governance Plane: z(t)** 
  * is for the Stewardship of a Data Product Supply Network of CATs represented as a Directed Acyclic Graph of Data Product Supply
  * **Control Plane: y(t)** 
    * is for the Networking of what is Produced as a result of Science & Engineering CATs
    * **Action Plane: x(t)** 
      * is for the Science & Engineering of Data Transformation as Computational Processing, a.k.a. CATs

**Multi-Agent Collaboration (MAC) for CATs using Content-Addressable Router (CAR)**

* _Design Description_
  * CATs and LangGraphs integration can enable a row wise business function as a Chart Tool of Multi-Agent Collaboration (MAC) if CAT Orders 
    act as a Transfer (Network) Function implemented as an OOP Command Pattern for which CATs Ingress and Egress sub-processes can be 
    executed by CATs’ Content-Addressable Router (CAR).
  * Architectural Considerations: CATs can inform business decisions given the following:
    * Action Plane: x(t)
      * CAT Functions can be defined as LangGraph Call Tools executed by LangGraphs Tool Node 
      * CAT Factory produces CAT Executors integrated with LangGraphs Tool Executor.
    * Control Plane: y(t) [aka Content-Addressable Router (CAR)]
      * CAR integrated with LangGraphs Router.
      * cadCAD (Network) Policies aka “Algorithmic Suggestions” can be deployed on LangGraphs Agent Nodes with specified Domain-Name 
        references as Rule Asset RIDs
    * Governance Plane: z(t)
      * A GreyBox Model for as a feature parameterized Tensor Field with process variable (PV) as label 
      * The business function is a CATs Control & Action Matrix - a 2 dimensional representation of 3 dimensional space
      