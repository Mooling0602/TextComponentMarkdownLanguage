# TCML 标准

## 语法

TCML是HTML的扩展版，语法参考Vue。

### 动态绑定值

如果需要将一个名为`example-attr`的attr绑定到一个Python对象上，那么:
无动态绑定: `<example example-attr="1234"></example>`
有动态绑定: `<example :example-attr="aPythonObject"></example>`

类似地，如果需要动态地传入一个值到模板里面:
无动态绑定: `<example>1234</example>`
有动态绑定: `<example>{{aPythonObject}}</example>`

和`f-string`一样，parser会自动从调用的作用域里获取那些值

### 行内数据

attr若为静态数据，默认会当做str解析。  
若那个值是一个Object，则遵循以下语法:  
`k:v,k2:v2,k3:'strValue'`
若是一个列表，则遵循以下语法:  
`v1,v2,v3,'strValue'`

> 必须使用**单引号**包裹字符串值(不包裹也可以)  
> 未被单引号包裹，会尽量作为能解析的最特殊的值解析

## 可用标签

### 通用

- `<line>`
- `<text>`
- - `<text-hover-text>`
- `<score>`
- `<selector>`
- - `<selector-separator>`
- `<keybind>`
- `<translate>`
- `<utranslate>`
- `<nbt>`
- `<click>`
- `<reset>`

#### text系

##### color快速标签

###### 原版颜色

- `<black>` 黑色  
- `<dark_blue>` 深蓝色  
- `<dark_green>` 深绿色  
- `<dark_aqua>` 湖蓝色  
- `<dark_red>` 深红色  
- `<dark_purple>` 紫色  
- `<gold>` 金色  
- `<gray>` 灰色  
- `<dark_gray>` 深灰色  
- `<blue>` 蓝色  
- `<green>` 绿色  
- `<aqua>` 天蓝色  
- `<red>` 红色  
- `<light_purple>` 粉红色  
- `<yellow>` 黄色  
- `<white>` 白色

##### style系快速标签

- `<bold>` **粗体**
- `<italic>` *斜体*
- `<underlined>` <u>下划线</u>
- `<strikethrough>` ~~删除线~~
- `<obfuscated>` ????乱码????

##### font系快速标签

- 默认 默认字体
- `<unifont>` Unifont字体
- `<uniform>` 同上
- `<alt>` 标准银河字母
- `<illageralt>` Minecraft Dungeons中使用的符文字体

## 通用 attr

### 样式

- `color` 指定颜色，值和颜色快速标签兼容
- `style` 指定样式，值和样式快速标签兼容，用逗号分割多个样式
- `font` 指定字体，值和字体快速标签兼容

### 悬浮

- `hover:text` 存在时为悬浮显示一些文字
- `hover:item` 若`hover:text`不存在，悬浮时显示一个物品，其值为物品数据
- `hover:entity` 若`hover:text`和`hover:item`都不存在，悬浮时显示一个实体，其值为实体的一些数据
  
[敬请参阅](https://zh.minecraft.wiki/w/Tutorial:%E6%96%87%E6%9C%AC%E7%BB%84%E4%BB%B6#%E6%82%AC%E5%81%9C%E4%BA%8B%E4%BB%B6%EF%BC%9AhoverEvent)

### 技术型

- `raw` 若此attr存在(值任意，可不带值存在)，将不继续解析此标签里面的标签，而是作为文本直接输出

## 标签特定 attr

### `<score>`

- `name` 计分板目标选择器
- `objective` 计分项名称

### `<selector>`

- `selector` 目标选择器内容
- `separator` 分割符。若`<selector>`标签内存在`<selector-separator>`标签，则忽略此attr

### `keybind`

- `keybind` 键位内容

### `translate`

- `translate` 本地化键名
- `fallback` 回落值
- `with` 一个列表

[敬请参阅](https://zh.minecraft.wiki/w/Tutorial:%E6%96%87%E6%9C%AC%E7%BB%84%E4%BB%B6#%E6%8C%89%E9%94%AE%E9%94%AE%E4%BD%8D%EF%BC%9Akeybind)

### `utranslate`

- `key` 本地化键名

### `nbt`

- `nbt` NBT路径
- `target:block` 目标方块
- `target:entity` 目标实体
- `target:storage` 目标存储
- `interpret` 是否将获取的值作为一个文本组件解析

> `target:*`优先级: `block`>`entity`>`storage`

[敬请参阅](https://zh.minecraft.wiki/w/Tutorial:%E6%96%87%E6%9C%AC%E7%BB%84%E4%BB%B6#NBT%E6%A0%87%E7%AD%BE%E7%9A%84%E5%80%BC%EF%BC%9Anbt)

### `click`

1. `action:open_url` 打开网页
2. `action:run_command` 运行指令
3. `action:change_page` 跳转页码
4. `action:suggest_command` 输入指令至聊天框
5. `action:copy_to_clipboard` 复制值到剪贴板

[敬请参阅](https://zh.minecraft.wiki/w/Tutorial:%E6%96%87%E6%9C%AC%E7%BB%84%E4%BB%B6#%E7%82%B9%E5%87%BB%E4%BA%8B%E4%BB%B6%EF%BC%9AclickEvent)
