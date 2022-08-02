# joomla-builder
An example repository equipped with a Joomla extension builder script for easy iteration.
<br><br>
### Best practice for utilizing this repo
1. **Create your own project repository first!!! Make sure it is BLANK**
2. Git clone the master/main branch of this `joomla-builder` repository
3. Select and copy from `joomla-builder` repo (to the root of your blank project repo) the following folders:
	4. **joomla-builder**
	5. **components**
	6. **plugins**
	7. **libraries**
	8. **modules**
4. Append the following text snippet *into* your project repository's `.gitignore` file:
<br>

```
# Exclude .DS_Store files
.DS_Store

# Ignore prettierrc
.prettierrc

# Python cache
__pycache__/

# JBuilder specific
builds/
```
<br>

### Next Steps:
* Either generate or write your extensions in their own subfolder inside the now existing extension-type folder of the relevant type `["components", "plugins", "libraries", "modules"]`
* For example if you wish to create and iterate on a `helloworld` component then create a folder called `helloworld` inside of the `components` folder in your (joomla-builder equipped) project repository. Write your extension files inside of that subfolder per Joomla standards.
* You may now easily create packaged installable artifacts of your new component by (in a terminal) changing to the `joomla-builder` folder and executing `./jBuilder.py`, you will find the generated/packages artifacts within the newly created `builds` folder.

**Note:** If you are not fluent with the creation of Joomla extensions like components and plugins, have a look at my other repository which generates absolute minimalist, ready to install (folders and zip artifacts), and customizable (via CLI arguments) components and plugins. That repository is: [joomla-tools](https://github.com/Node0/joomla-tools) `https://github.com/Node0/joomla-tools`  
<br>
You may then move the generated folder of the component or plugin (if you use joomla-tools to create it) into your project folder (as prepared using these instructions).  
At that point you are all set to freely develop your extension, and execute `./jBuilder.py` everytime you would like to do a test install iteration.
<br><br>
**Note 2:**
*You'll want to stage->commit->push etc your changes as you go according to git best practices.*