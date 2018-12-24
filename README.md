### 基于代码生成的简单模板引擎

### install

```sh
pip3 install simpletemplate
```

```python
from simpletemplate import Template

Template("Hello, {{name}}!").render({'name': 'world'})
```

#### 模板语法 

```sh

%{fields = jclass.fields}%

private {{jclass.name}}(Builder builder) {
    %{for field in fields:}%
    this.{{field.name}} = builder.{{field.name}};
    %{end}%
}

public static class Builder {

    %{for field in fields:}%
    private {{field.jtype}} {{field.name}} = null;
    %{end}%

    %{for field in fields:}%
    %{if field.comment:}%
    /**
     * {{field.comment}}
     */
     %{end}%
    public Builder set{{field.name.title()}}({{field.jtype}} {{field.name}}) {
        this.{{field.name}} = {{field.name}};
        return this;
    }

    %{end}%
    public {{jclass.name}} build() {
        return new {{jclass.name}}(this);
    }
}
```

#### 测试代码

```python
'''
interface 
'''

def test_template():
    class Obj:
        pass

    def jfield(jtype: str, name: str, *, modifier: str = '', init_value: str = '', comment: str = ''):
        field = Obj()
        field.modifier = modifier
        field.jtype = jtype
        field.name = name
        field.initial_value = init_value
        field.comment = comment

        return field

    data = Obj()
    data.name = 'ShareConfig'
    data.fields = []
    data.fields.append(jfield('Tencent', 'tencent', modifier='private final'))
    data.fields.append(
        jfield('IWXApi', 'wxApi', modifier='private final', comment='wechat share'))

    print(Template(TMPL_BUILDER).render({'jclass': data}))


if __name__ == '__main__':
    test_template()
```

#### generated Java Code

```java

private ShareConfig(Builder builder) {
    this.tencent = builder.tencent;
    this.wxApi = builder.wxApi;
}

public static class Builder {

    private Tencent tencent = null;
    private IWXApi wxApi = null;

    public Builder setTencent(Tencent tencent) {
        this.tencent = tencent;
        return this;
    }

    /**
     * wechat share
     */
    public Builder setWxapi(IWXApi wxApi) {
        this.wxApi = wxApi;
        return this;
    }

    public ShareConfig build() {
        return new ShareConfig(this);
    }
}
```