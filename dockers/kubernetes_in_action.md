# 3 Pods: running containers in Kubernetes
Containers are designed to run only a single process per container (unless the process itself spawns child processes).

A pod of containers allows you to run closely related processes together and provide them with (almost) the same environment as if they were all running in a single container, while keeping them somewhat isolated.

Kubernetes achieves this by configuring Docker to have all containers of a pod share the same set of Linux namespaces instead of each container having its own set.

One thing to stress here is that because containers in a pod run in the same Network namespace, they share the same IP address and port space.

All pods in a Kubernetes cluster reside in a single flat, shared, network-address space

You should think of pods as separate machines, but where each one hosts only a certain app. 

Using multiple namespaces allows you to split complex systems with numerous components into smaller distinct groups. They can also be used for separating resources in a multi-tenant environment, splitting up resources into production, development, and QA environments, or in any other way you may need.

# 4 Replication and other controllers: deploying managed pods

In real-world use cases, you want your deployments to stay up and running automatically and remain healthy without any manual intervention. To do this, you almost never create pods directly. Instead, you create other types of resources, such as ReplicationControllers or Deployments, which then create and manage the actual pods.

To make sure your app is restarted on another node, you need to have the pod managed by a ReplicationController or similar mechanism

Initially, ReplicationControllers were the only Kubernetes component for replicating pods and rescheduling them when nodes failed. Later, a similar resource called a ReplicaSet was introduced. It’s a new generation of ReplicationController and replaces it completely (ReplicationControllers will eventually be deprecated).

You should always create ReplicaSets instead of ReplicationControllers from now on. You usually won’t create them directly, but instead have them created automatically when you create the higher-level Deployment resource

A ReplicaSet behaves exactly like a ReplicationController, but it has more expressive pod selectors

DaemonSets run only a single pod replica on each node, whereas ReplicaSets scatter them around the whole cluster randomly

ReplicationControllers, ReplicaSets, and DaemonSets run continuous tasks that are never considered completed

Kubernetes includes support for this through the Job resource, which is similar to the other resources we’ve discussed in this chapter, but it allows you to run a pod whose container isn’t restarted when the process running inside finishes successfully. Once it does, the pod is considered complete.

Job resources run their pods immediately when you create the Job resource. But many batch jobs need to be run at a specific time in the future or repeatedly in the specified interval. In Linux- and UNIX-like operating systems, these jobs are better known as cron jobs. Kubernetes supports them, too. A cron job in Kubernetes is configured by creating a CronJob resource. The schedule for running the job is specified in the well-known cron format, so if you’re familiar with regular cron jobs, you’ll understand Kubernetes’ CronJobs in a matter of seconds

# 5 Services: enabling clients to discover and talk to pods

A Kubernetes Service is a resource you create to make a single, constant point of entry to a group of pods providing the same service.

As you’ve seen, a service can be backed by more than one pod. Connections to the service are load-balanced across all the backing pods. But how exactly do you define which pods are part of the service and which aren’t?

Up to now, we’ve talked about services backed by one or more pods running inside the cluster. But cases exist when you’d like to expose external services through the Kubernetes services feature. Instead of having the service redirect connections to pods in the cluster, you want it to redirect to external IP(s) and port(s).

Services don’t link to pods directly. Instead, a resource sits in between—the Endpoints resource.

If you create a service without a pod selector, Kubernetes won’t even create the Endpoints resource (after all, without a selector, it can’t know which pods to include in the service). It’s up to you to create the Endpoints resource to specify the list of endpoints for the service.

Up to now, we’ve only talked about how services can be consumed by pods from inside the cluster. But you’ll also want to expose certain services, such as frontend webservers, to the outside, so external clients can access them

# 6 Volumes: attaching disk storage to containers

Every new container starts off with the exact set of files that was added to the image at build time. Combine this with the fact that containers in a pod get restarted (either because the process died or because the liveness probe signaled to Kubernetes that the container wasn’t healthy anymore) and you’ll realize that the new container will not see anything that was written to the filesystem by the previous container, even though the newly started container runs in the same pod.

Kubernetes provides this by defining storage volumes. They aren’t top-level resources like pods, but are instead defined as a part of a pod and share the same lifecycle as the pod.