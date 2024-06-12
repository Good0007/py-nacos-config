## 如何使用

- 安装依赖
```bash
pip3 install py-nacos-config
```

- 初始化配置
```python
from py_nacos_config.nacos import NacosClient, NacosConfigReader

if __name__ == "__main__":
    nacos = NacosClient("localhost:8848", 'nbchat-dev')
    # config_type: text/yaml/properties/json
    config = NacosConfigReader(nacos, data_id="test_config", group="test", config_type='yaml').load_config(debug=True)
    print(config)
    print(config.get("test"))
    # 也可以使用环境变量设置参数，支持的key值参考：
```

- 环境变量设置
```python
# 环境变量说明：
# 
# nacos地址
ENV_KEY_NACOS_SERVER_ADDR = "NACOS_SERVER_ADDR"
# 用户名
ENV_KEY_NACOS_USERNAME = "NACOS_USERNAME"
# 密码
ENV_KEY_NACOS_PASSWORD = "NACOS_PASSWORD"
# 命名空间
ENV_KEY_NACOS_NAMESPACE = "NACOS_CONFIG_NAMESPACE"
# 配置ID
ENV_KEY_NACOS_CONFIG_DATA_ID = "NACOS_CONFIG_DATA_ID"
# 配置分组
ENV_KEY_NACOS_CONFIG_GROUP = "NACOS_CONFIG_GROUP"
# 配置标签
ENV_KEY_NACOS_CONFIG_TAG = "NACOS_CONFIG_TAG"
# 配置类型 text/yaml/properties/json
ENV_KEY_NACOS_CONFIG_TYPE = "NACOS_CONFIG_TYPE"

```