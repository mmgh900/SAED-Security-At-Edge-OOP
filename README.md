# SAED-Security-At-Edge
SAED is an edge-based platform that offers intelligence in the form of privacy-preserving semantic and personalized search at the edge tier to augment the capabilities of the Enterprise Search services on the cloud. SAED can be plugged in to any cloud-based enterprise search solution (e.g., AWS Kendra) and extend their smartness and privacy wihtout enforcing any change on them. SAED is the first platform that develops the idea of **logical partitioning of applications across edge-to-cloud continuum** in the context of a privacy-preserving search application. In particular, to preserve the user's privacy, SAED decouples the intelligence aspect of the semantic search algorithm (and performs it on a trusted edge tier) from its pattern matching aspect (that is performed on the untrusted public cloud tier).

## Availability
SAED is an open-source program that was developed at HPCC lab, University of Louisiana Lafayette. Details of its theory, implementation, and evaluation have been published in 21st IEEE/ACM International Symposium on Cluster, Cloud, and Grid Computing (CCGrid 2021) in Melbourne, Australia. 
The research paper is also available on the arXiv repository:
https://arxiv.org/abs/2102.13367

 
## Architecture

Architectural overview of SAED within the edge tier and (as part of the three-tier enterprise search service) is shown below. SAED provides semantic search via identifying the query context (Context Identifier module) and combining that with the user’s interests (Interest Detector module). Then, the Query Expansion module and the Weighting unit of SAED, respectively, incorporate the semantic and assure the relevancy of the results. Solid and dashed lines indicate the interactions from the user to the cloud tier and from the cloud tier to the user, respectively.
<p align="center"><img src="archi.png"></p>

## Running SAED on AWS Kendra
### Dependencies
Running SAED needs the following dependencies:
 ```python>=3.5```
 ```pyenchant==3.2.0```
 ```gensim==3.8.3```
 ```numpy==1.14.2```
 ```nltk==3.2.5```
 ```pywsd>=1.2.0```
 ```yake==0.4.6```
 ```wn>=0.0.19```
 ```six>=1.11.0```
 ```pandas>=0.22.0```
 
Please refer to Step #2 from the below instructions to install the dependencies.

