##HTML

Modern websites are made in html 5.

###Tags

Creating Elements

- h1 is html element(Heading Biggest)
- <> are called tags, represents elements
- <p> saad </p> Paragraph tags, Opening tags and closing tags, saad is element.
- <span></span> Same Line.

Example
<p> I am Saad </p>
<span> I am teaching </span>

### HTML and Trees

- <div></div>: used to group content together.

'''
<div>
    <h1>Article Title </h1>
    <p>This is a paragrah</p>
</div>
'''

- <p><strong></strong></p>: For bold text

-<p><em></em></p>: For italics text

###HTML Doctypes


- Button
```
<button>a button!</button>

```

- Unordered List
```
    <ul>
      <li>HTML</li>
      <li>CSS</li>
      <li>JavaScript</li>
    </ul>
```

- Hyperlinks
```
<a href="https://www.udacity.com">Udacity</a>
```

- Image Source

alt: Alternative Description
```
<img src="http://somewebsite.com/image.jpg" alt="short description">
```

- Path
If there is a file called index.html in a directory and there is another directory called example/ in the same directory.
```
<a href="example/filename.html">Example Path</a>
```

- Local Path
```
<a href="/Users/cameron/Udacity/etc/labs/fend/example/hello-world.html"> Hello, world!</a>

```

- External Path
```
<a href="http://labs.udacity.com/fend/example/hello-world.html">Hello, world!</a>

```

- Relative Path
```
<a href="physics/relativity.html">Einstein's Special Relativity</a>
```

- Figures

```
<!DOCTYPE html>
<html lang="en">
<body>
  <figure>
    <img src="redwoods_state_park.jpg" alt="Redwoods state park">
  </figure>
    <figcaption>Stout Memorial Grove in Jedediah Smith Redwoods State Park in 2011 by Chmee2 (Own work) GFDL or CC BY-SA 3.0, via Wikimedia Commons - <a href="https://commons.wikimedia.org/wiki/File%3AStout_Memorial_Grove_in_Jedediah_Smith_Redwoods_State_Park_in_2011_(22).JPG">Source</a>
    </figcaption>
</body>
</html>
```

###Mockup Website
```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Web Dev Blog Post</title>
</head>
<body>
  <!-- Format the text below! When you're done, you can click over to solution.html to see how I did it.
-->
  <h1>Hottest Jobs in 2016 #2: Web Developer</h1>

  <h4>By <strong><em>Christopher Watkins</strong></em></h4>

  <h5>January 19, 2016</h5>

  <img
       src="http://i1.wp.com/blog.udacity.com/wp-content/uploads/2016/01/Slack-for-iOS-Upload.jpg?zoom=2&amp;resize=320%2C168">

  LOTS of demand. 🔥
</body>
</html>
```

##CSS Syntax (Cascading Style Sheet)

- All CSS goes inside <style></style> which goes inside <head></head>.
- All CSS design starts with rule set called selector (div).
- Declaration block decides how the styling will look like.

```
div {
    text-align: right;
}
```

- Styling Example
```
<head>
    <style>
        p {
            color: blue;
        }
        h1 {
            color: red;
        }
    </style>
</head>
<body>
    <h1> Hello boi </h1>
    <p>This is my life.</p>
</body>
```

- Comments

CSS Comments
```
p {
    color: blue;
}
/* add CSS here */
h1 {
    color: red;
}

```

HTML Comments <!-- This is a comment -->)
```
<!-- This is a comment -->
<div class="example">Words, words, words.</div>

```

### Attributes and Selectors

- Tag Selector
```
h1 {
  color: green;
}
```

- Class Attribute Selector
```
.book-summary {
  color: blue;
}
```

- Id attribute Selector
```
#site-description {
  color: red;
}
```

Example
```
<head>
    <style>
        /* For Class */
        .para_description {
            color: blue;
        }
        /* For id */
        #site_description {
            color: red;
        }

    </style>
</head>
<body>
    <h1> Hello boi </h1>
    <p id="site_description"> Hello world </p>
    <p class="para_description">This is my life.</p>
</body>
```

```
    /* In CSS */
 .right {
    text_align: right;
 }

    <-In HTML ->
 <div class="right"></div

 or

 <p class="highlight module right"></p>

```

- Reference: CSS tricks or mozrilla

- CSS Italics
```
h2 {
font-style:roman;
}
```

- CSS Underline
```
h3 {
    text-decoration: underline;
}
```

- CSS Uppercase
```
h3 {
    text-transform: ;
}
```

- CSS Bold
```
h3 {
    font-weight: ;
}
```

- CSS Units
Can be Absolute (px, in) or Relative (%, vm)

Set the first div's width to 100px (pixels)
Set the second div's height to 200px (pixels)
Set the third div's margin to 1em
Set the fourth div's font-size to 2em

```
<html>
<head>
    <title> Quiz - Units in CSS</title>
    <style>
        .first {
            width: 100px;
        }
        .second {
            height: 200px;
        }
        .third {
            margin:1em;
        }
        .fourth {
            font-size:2em;
        }
    </style>
</head>
</html>
```

### CSS Colors

- RGB
Red 0-255
Green 0-255
Blue 0-255

```
body {
    background-color: rgb(255, 0, 255);
}
```

- Hexademical
Red 00-FF
Green 00-FF
Blue 00-FF

body {
    background-color: #ff00fff;
}

- Font
```
.h2 {
    font-family: Helvetica, Arial, sans-serif;
}
```

- Link CSS Attributes with html class and identity

```
<!DOCTYPE html>
<html>
<head>
  <title>Writing Selectors Exercise</title>
  <style>
    /* missing id */
      #menu{
      text-align: center;
    }

    /* missing class */
      .item{
      color: red;
    }

    /* missing class */
      .picture{
      border-radius: 5px;
    }

    /* missing class */
      .description{
      font-style: italic;
    }
  </style>
</head>
<body>
  <div id="menu">
    <h1 class="item">Chicken Clay Pot</h1>
    <img src="img/clay-pot.jpg" alt="clay pot" class="picture">
    <p class="description">Crispy rice baked in clay pot topped with chicken and vegetables</p>
  </div>
</body>
</html>
```