<?php
include 'config.php';

$clientId = 'toDatabase';
$topic  = '/topic/intermediateReportTopic';

if (!$config) {
    return false;
}

$connection = mysqli_connect($config['host'], $config['username'], $config['password']);  
mysqli_select_db($connection,$config['database']);

try {
    $stomp = new Stomp('tcp://192.99.113.10:61613','system','manager', array('client-id'=> $clientId ));
} catch(StompException $e) {
    die('Connection failed: ' . $e->getMessage());
}

$isSubscribe = $stomp->subscribe($topic);

while($isSubscribe) {
    if ($stomp->hasFrame()) {
        $frame = $stomp->readFrame();
        if ($frame != NULL) {
            $d = json_decode($frame->body);
            $sql = "INSERT into reports(symbol,date,openPrice,highPrice,lowPrice,closePrice,volume,vwap,ema,relativeVolume,"
                . "trend,tradePosition,entryPrice,entryPriceWithCushion,sl,slWithCushion,plPoints,exitPrice,target1Pos,"
                . "target1Entry,target1Price,target1Exit,target1PL,target2Pos,target2Entry,target2Price,target2Exit,target2PL) "
                . "values('$d->symbol','$d->date','$d->openPrice','$d->highPrice','$d->lowPrice','$d->closePrice',"
                . "'$d->volume','$d->vwap','$d->ema','$d->relativeVolume','$d->trend','$d->tradePosition','$d->entryPrice',"
                . "'$d->entryPriceWithCushion','$d->sl','$d->slWithCushion','$d->plPoints','$d->exitPrice','$d->target1Pos',"
                . "'$d->target1Entry','$d->target1Price','$d->target1Exit','$d->target1PL','$d->target2Pos',"
                . "'$d->target2Entry','$d->target2Price','$d->target2Exit','$d->target2PL');";

            $result = mysqli_query($connection,$sql);
            flush();
            $stomp->ack($frame);
        }
    }
    sleep(1);
}
if($isSubscribe){
    $stomp->unsubscribe($topic);
    unset($stomp);
}