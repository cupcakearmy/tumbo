# tumbo

Docker matrix build generator

```yaml
variables:
    my_var:
        - a
        - b
        - c
    some_other:
        - 0.1.0
        - 0.1.2

context: ./build
recipe: './Dockerfile.j2'
tag: "my-tag:{{ my_var }}-{{ some_other }}"

parallel: no
# no
# yes : uses all threads available
# n : number of threads to use
# default: yes

push: yes
run: yes
registry:
    username: my_user
    password: my_pass
    host: my_host
```

### Config Reference

#### Variables

The variables to build the matrix. Simply specify an array for each variable. They will be available in the template.

```yaml
variables:
    my_var:
        - a
        - b
        - c
    some_other:
        - 0.1.0
        - 0.1.2
```

#### Recipe

The template to compile the dockerfile. Can be a template itself if you don't want to write everything in the same file.

###### Simple

```yaml
recipe: './Dockerfile.j2'
```

###### Template

```yaml
variables:
    my_var:
        - a
        - b

recipe: './{{ my_var }}.j2'
```

Assuming `my_var` hast the values `a` and `b` it will render to `./a.j2` and `./b.j2` accordingly.

#### Context (Optional)

**Default:** directory of the config file.

Specify the directory where the templates and the dockerfiles will be built.
Supports both absolute and relative paths.

```yaml
context: ./build
```

#### Tag (Optional)

**Default:** Creates a tag that includes all variables.
In most cases it will not be necessary to specify, but can be usefull if your are pushing images. Supports templating of course.

**Important:** The tag should be unique across the matrix, otherwise you will overwrite other tags. So always include all the variables you specified inside the image name

```yaml
variables:
    var1:
        - a
        - b
    var2:
        - a
        - b
    var3:
        - a
        - b

tag: 'my-image-name:{{ var3 }}-{{ var1 }}-{{ var2 }}'
```
