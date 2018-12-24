from simpletemplate import Template

'''
inner template
'''

TMPL_BUILDER = '''\

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
'''

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
