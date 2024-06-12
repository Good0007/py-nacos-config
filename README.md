## 如何使用

### 安装依赖
```bash
npm install pynacosconfig
```

### 读取配置

```python
from py_nacos_config.nacos import NacosClient, NacosConfigReader

if __name__ == "__main__":
    nacos = NacosClient("localhost:8848", 'nbchat-dev')
    config = NacosConfigReader(nacos, data_id="test_config", group="test", config_type='yaml').load_config(debug=True)
    print(config)
# 也可以使用环境变量设置参数，支持的key值参考 py_nacos_config/constants.py
```