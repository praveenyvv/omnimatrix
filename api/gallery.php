<?php
header('Content-Type: application/json');
header('Cache-Control: no-cache, no-store, must-revalidate');

$baseDir = dirname(__DIR__); // project root
$assetsDir = $baseDir . DIRECTORY_SEPARATOR . 'website-assets';

$galleryMap = [
    'lab-products'     => '3-Products-Laboratory-Plasticware',
    'injection-molds'  => '4-Services-Injection-Molds',
    'press-tools'      => '5-Services-Press-Tools',
    'die-casting'      => '6-Services-Die-Casting',
    'jigs-fixtures'    => '7-Services-Jigs-Fixtures',
    'spm-automation'   => '8-Services-SPM-Automation',
    'service1-gallery' => '4-Services-Injection-Molds',
    'service2-gallery' => '5-Services-Press-Tools',
    'service3-gallery' => '6-Services-Die-Casting',
    'service4-gallery' => '7-Services-Jigs-Fixtures',
    'service5-gallery' => '6-Services-Die-Casting',
    'service6-gallery' => '8-Services-SPM-Automation',
];

$allowedExts = ['jpg', 'jpeg', 'png', 'webp', 'gif'];
$manifest = [];
$v = time();

foreach ($galleryMap as $key => $folderName) {
    $folderPath = $assetsDir . DIRECTORY_SEPARATOR . $folderName;
    $images = [];

    if (is_dir($folderPath)) {
        $files = scandir($folderPath);
        sort($files);
        foreach ($files as $file) {
            if ($file === '.' || $file === '..') continue;
            $ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
            if (in_array($ext, $allowedExts)) {
                // Relative path for pages/ directory
                $images[] = '../website-assets/' . $folderName . '/' . $file . '?v=' . $v;
            }
        }
    }
    $manifest[$key] = $images;
}

echo json_encode($manifest, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
