# tumbo

Docker matrix build generator.

The basic idea is that you combine a config file with custom variables with templating (Jinja2) and *__tumbo__* will run your matrix build in docker.

## 📦 Install

```
pip install tumbo
```

## 🚀 Quickstart

###### spec.yml

```yaml
variables:
    version:
        - 3.11
        - 3.10
        - 3.9
    name:
        - Alice
        - Bob

recipe: ./Dockerfile.j2

run: yes
parallel: no
```

###### Dockerfile.j2

```
FROM alpine:{{ version }}

CMD [ "echo", "Hi {{ name }} from {{ version }}" ]
```

And run

```sh
tumbo spec.yml
```

Tumbo will then generate 6 images, build and run them in all the combinations possible with the variables given.

## 🐣 [Examples](https://github.com/cupcakearmy/tumbo/tree/master/examples)

Have a look at the [examples folder]((https://github.com/cupcakearmy/tumbo/tree/master/examples)). I think it's the fastest way to learn

## 📘 Config Reference

### Variables

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

### Recipe

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

### Context (Optional)

**Default:** directory of the config file.

Specify the directory where the templates and the dockerfiles will be built.
Supports both absolute and relative paths.

```yaml
context: ./build
```

### Tag (Optional)

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

### Parallel (Optional)

**Default:** yes

Whether the builds/push/runs should run in parallel or after each other.

###### no

Parallel off.

```yaml
parallel: no
```


###### yes

Uses all the threads available on the machine.

```yaml
parallel: yes
```


###### number

Uses how many thread you specify

```yaml
parallel: 2
```

### run (Optional)

**Default:** no

Wether to run the docker image after building. Can be usefull if running automated tests.

```yaml
run: yes
```

### push (Optional)

**Default:** no

Wether to push the docker image after building.
Can be used to push images to the docker registry (or your own).
See below on how to login.

```yaml
run: yes
```

### registry (Optional)

**Default:** Empty

Credentials for `docker login`. Used to push images and to specify a custom registry if necessary.

```yaml
registry:
    username: my_user
    password: my_pass
    host: my_host
```
