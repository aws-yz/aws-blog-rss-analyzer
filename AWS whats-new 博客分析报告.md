AWS whats-new 博客分析报告

**分析时间范围**: 2025 年 08 月 22 日 至 2025 年 08 月 22 日
**文章总数**: 4
**生成时间**: 2025-08-24 16:59:03

## 博客文章列表

### 1. Amazon EKS enables namespace configuration for AWS and Community add-ons

- **作者**: AWS Team
- **发布时间**: 2025 年 08 月 22 日
- **链接**: https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-eks-namespace-configuration-addons

**中文摘要**:

# Amazon EKS 支持 AWS 和社区插件的命名空间配置

Amazon EKS 现已支持 AWS 和社区插件的 Kubernetes 命名空间配置功能，为用户提供了更强大的集群内插件组织管理能力。该功能允许用户在安装插件时指定自定义命名空间，实现 EKS 集群内插件对象的更好组织和隔离。这种灵活性使用户能够将插件与其运维需求和现有的命名空间策略保持一致，提升资源管理效率。

值得注意的是，一旦插件安装在特定命名空间中，若需更改其命名空间，必须先移除再重新创建该插件。用户可通过 AWS 管理控制台、Amazon EKS API、AWS CLI 以及 AWS CloudFormation 等基础设施即代码工具使用此功能。该特性已在所有商业 AWS 区域推出，为 Kubernetes 集群管理提供了更精细的控制能力。

---

### 2. Amazon RDS for PostgreSQL now supports delayed read replicas

- **作者**: AWS Team
- **发布时间**: 2025 年 08 月 22 日
- **链接**: https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-rds-postgresql-delayed-replica

**中文摘要**:

# Amazon RDS for PostgreSQL 推出延迟读取副本功能

Amazon RDS for PostgreSQL 现已支持延迟读取副本功能，允许用户指定副本数据库落后于源数据库的最小时间周期。该功能创建了一个时间缓冲区，有效防护因误操作导致的数据丢失，如意外删除表或数据错误修改。在灾难恢复场景中，管理员可以在问题变更应用前暂停复制，将复制恢复到特定日志位置，并将副本提升为新的主数据库。相比传统的时间点恢复操作（对大型数据库可能需要数小时），此方法能显著加快恢复速度。该功能已在所有提供 RDS for PostgreSQL 的 AWS 区域部署，包括 AWS GovCloud（美国）区域，无需额外费用，仅按标准 RDS 定价收费。这一技术增强了 PostgreSQL 数据库的灾备能力和数据安全性。

---

### 3. Amazon EC2 R7g instances now available in Africa (Cape Town)

- **作者**: AWS Team
- **发布时间**: 2025 年 08 月 22 日
- **链接**: https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-ec2-r7g-instances-africa-cape-town/

**中文摘要**:

# Amazon EC2 R7g 实例现已在非洲（开普敦）地区推出

亚马逊云科技宣布 EC2 R7g 实例现已在 AWS 非洲（开普敦）区域正式可用。这些实例由 AWS Graviton3 处理器提供支持，相比 Graviton2 处理器性能提升高达 25%，并基于 AWS Nitro 系统构建，提供高效、灵活且安全的云服务。R7g 实例在保持相同性能的同时，能够比同类 EC2 实例减少高达 60%的能源消耗，有效降低云计算碳足迹。

为满足不同规模需求，R7g 实例提供 9 种不同规格（包括裸金属实例），支持高达 30Gbps 的网络带宽和 20Gbps 的 Amazon EBS 带宽。企业可通过 AWS Graviton Fast Start 计划和 Graviton 迁移顾问工具，轻松将工作负载迁移至基于 Graviton 的实例，充分利用其卓越性能和

---

### 4. Amazon RDS for Db2 now supports read replicas

- **作者**: AWS Team
- **发布时间**: 2025 年 08 月 22 日
- **链接**: https://aws.amazon.com/about-aws/whats-new/2025/08/amazon-rds-for-db2-read-replicas/

**中文摘要**:

# Amazon RDS for Db2 现已支持只读副本功能

Amazon RDS for Db2 现已推出只读副本功能，允许用户为数据库实例添加最多三个只读副本。这些副本通过异步复制方式接收主数据库的变更，使客户能够将读取操作分流到副本上，有效降低主数据库的负载压力。用户可以在同区域或跨区域部署这些副本，为读密集型应用提供更高性能支持。此功能还可作为灾难恢复解决方案，通过将只读副本提升为支持读写操作的实例来确保业务连续性。需要注意的是，副本实例的所有 vCPU 都需要 IBM Db2 许可证，客户可以从 AWS Marketplace 获取按需许可，或使用自带许可(BYOL)模式。这一功能增强了 RDS for Db2 的可扩展性和可用性，为企业级数据库应用提供了更灵活的部署选项。

---

⋮
● Completed in 55.866s

> 完美！现在系统能够智能地根据博客类型选择最佳的内容源：

1. What's New/News: 使用 descripti
