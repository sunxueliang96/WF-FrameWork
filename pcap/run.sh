#!/bin/bash
my_name="898e44bdc756"
echo "running ",${my_name}

docker start ${my_name}
docker exec ${my_name} firefox target
#忘光了、写不来shell了
先用python写，回头换成shell
另外我们是不是可以在识别website的时候，也许多做一点，例如识别动作，我是看视频挂机呢还是疯狂操作，也许
