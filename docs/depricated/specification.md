### Specification:

...

Ray is deployed as an execution middleware on top of [Bacalhau’s](https://www.bacalhau.org/) [Compute Over Data (CoD)](https://github.com/bacalhau-project/bacalhau). 
CoD enables IPFS to serve as CATs' Data Mesh's network layer to provide parallelized data ingress and egress for IPFS 
data. This portability closes the gap between data analysis and business operations by connecting the network planes of 
the cloud service model (SaaS, PaaS, IaaS) with IPFS. CATs connect these network planes by enabling the instantiation of 
FaaS with cloud services in AWS, GCP, Azure, etc. on a **Data Mesh** network of CATs. CoD enables this connection as p2p 
distributed-computing job submission in addition to the client-server job submission provided by Ray.
![alt_text](images/simple_CAT2b.jpeg)