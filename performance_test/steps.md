## 3. The Fundamentals of Effective Application Performance Testing

考虑以下9个问题来准备性能测试。比如第一条，确保被测试的软件是可测试的，可测试的标准是功能完整可用且每个功能没有明显的性能问题（比如响应时间过长）；第二条，为性能测试预留充足的时间，为测试的各个阶段分配一段时间；第三条，冻结代码，确保被测试的软件与代码是一致的；第四条，根据生产环境模拟测试环境，测试环境的结构组成应该与生产环境的一致，2个环境的主要区别是测试环境的资源数量相对来说较少，因此在分析测试报告时，需要考虑资源少而引发低性能的可能性；第五条，设置测试目标，比如响应时间，线上服务持续时间，需要与各个团队的相关负责人（也就是stakeholders）达成一致；第六点，根据需求确定用例，根据每一个用例编写对应的测试脚本；第七点，提供测试数据，也就是确定每一个测试用例的输入数据，输出数据，同时需要考虑如何将生产环境的数据拷贝到测试环境以及数据量大的时候如何处理，还需要考虑如何确保数据的安全性，确保用户的账号密码，邮箱信息是处理过的，否则会泄漏这些关键信息；第八点，如何更加真实地测试软件，这需要使用不同的测试类型，比如Volume Test， Smoke Test等，模拟不同的用户数量，比如同时模拟1000个用户使用该软件，或者每隔一段时间增加25个用户之类的行为。

1. Making Sure Your Application Is Ready
2. Allocating Enough Time to Performance Test
3. Obtaining a Code Freeze
4. Designing a Performance Test Environment
* Virtualization
* Cloud Computing
* Load Injection Capacity
* Addressing Different Network Deployment Models
* Environment Checklist
* Software Installation Constraints
5. Setting Realistic Performance Targets
* Consensus
* Performance Target Definition
* Network Utilization
* Server Utilization
6. Identifying and Scripting the Business-Critical Use Cases
* Use-Case Checklist
* Use-Case Replay Validation
* What to Measure
* To Log In or Not to Log In
* Peaceful Coexistence
7. Providing Test Data
* Input Data
* Target Data
* Session Data
* Data Security
8. Ensuring Accurate Performance-Test Design
* Principal Types of Performance Test
* The Load Model
* Think Time
* Pacing
9. Identifying the KPIs
* Server KPIs
* Network KPIs
* Application Server KPIs

以上9点就是下面提到的NFRs，根据以上9点可以指定一个测试计划，每一个项目都会对应一个测试计划，每一个测试计划可以划分成有序的步骤（具体需要看第四章内容）。

## 4. The Process of Performance Testing

In Chapter 3, my intention was to cover nonfunctional requirements (NFRs) in a logical but informal way. This chapter is about using these requirements to build a test plan: a performance testing checklist divided into logical stages as shown bekow:

Step 1: Nonfunctional Requirements Capture
Step 2: Performance Test Environment Build
Step 3: Use-Case Scripting
Step 4: Performance Test Scenario Build
Step 5: Performance Test Execution
Step 6: Post-Test Analysis and Reporting

阶段一，搜集被测试软件的信息，准备测试所依赖的条件，这一阶段的工作事项有：

* Deadlines available to complete performance testing, including the scheduled deployment date.
* Internal or external resources to perform the tests. This decision will largely depend on time scales and in-house expertise (or lack thereof).
* Test environment design. Remember that the test environment should be as close an approximation of the live environment as you can achieve and will require longer to create than you estimate.
* A code freeze that applies to the test environment within each testing cycle.
* A test environment that will not be affected by other user activity. Nobody else should be using the test environment while performance test execution is taking place; otherwise, there is a danger that the test execution and results may be compromised.
* Identified performance targets. Most importantly, these must be agreed to by appropriate business stakeholders. See Chapter 3 for a discussion on how to achieve stakeholder consensus.
* Key use cases. These must be identified, documented, and ready to script. Remember how vital it is to have correctly identified the key use cases to script. Otherwise, your performance testing is in danger of becoming a wasted exercise.
* Parts of each use case (such as login or time spent on a search) that should be monitored separately. This will be used in Step 3 for checkpointing.
* The input, target, and session data requirements for the use cases that you select. This critical consideration ensures that the use cases you script run correctly and that the target database is realistically populated in terms of size and content. As discussed in Chapter 3, quality test data is critical to performance testing. Make sure that you can create enough test data of the correct type within the timeframes of your testing project. You may need to look at some form of automated data management, and don’t forget to consider data security and confidentiality.
* A load model created for each application in scope for performance testing.
* Performance test scenarios identified in terms of the number, type, use-case content, and virtual user deployment. You should also have decided on the think time, pacing, and injection profile for each use-case deployment.
* Identified and documented application, server, and network KPIs. Remember that you must monitor the hosting infrastructure as comprehensively as possible to ensure that you have the necessary information available to identify and resolve any problems that may occur.
* Identified deliverables from the performance test in terms of a report on the test’s outcome versus the agreed-upon performance targets. It’s a good practice to produce a document template that can be used for this purpose.
* A defined procedure for submitting any performance defects discovered during testing cycles to the development or application vendor. This is an important consideration that is often overlooked. What happens if you find major application-related problems? You need to build contingency into your test plan to accommodate this possibility. There may also be the added complexity of involving offshore resources in the defect submission and resolution process. If your plan is to carry out the performance testing using in-house resources, then you will also need to have the following in place:
* Test team members and reporting structure. Do you have a dedicated and technically competent performance testing team? Often organizations hurriedly put together such teams by grabbing functional testers and anyone else unlucky enough to be available. To be fair, if you have only an intermittent requirement to performance test, it’s hard to justify keeping a dedicated team on standby. Larger organizations, however, should consider moving toward establishing an internal center of testing excellence. Ensure at the very minimum that you have a project manager and enough testing personnel assigned to handle the scale of the project. Even large-scale performance testing projects rarely require more than a project manager and a couple of engineers. Figure 4-1 demonstrates a sample team structure and its relationship to the customer.
* The tools, resources, skills, and appropriate licenses for the performance test. Make sure the team has what it needs to test effectively.
* Adequate training for all team members in the tools to be used. A lack of testing tool experience is a major reason why many companies’ introduction to performance testing is via an outsourced project.