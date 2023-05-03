# How it works?

由于整体流程涉及到IO密集+CPU计算密集型的任务，所以整体思路是使用多进程（`concurrent.futures.ProcessPoolExecutor`）的方式来进行数据处理，尽可能利用到多个进程并行处理：

1. 使用`concurrent.futures.ProcessPoolExecutor`开启进程池（默认是CPU核数）；
2. 多个进程workers同时进行读取文件并且过滤文件，并按日期（从`timestamp`字段转换而来）对结果进行分类，输出一个`dictionary`（日期作为`key`，存放记录的list作为`value`）；
3. 每次有进程输出结果，主进程会将结果进行一个合并操作；
4. 读取和过滤的操作结束后，将`dictionary`的`values`再次交给多个workers进程同时进行排序和文件输出；
5. 输出结果


# Result

多次测试的结果，在8核16G内存的电脑上，程序花费的时间在33s～45s这个区间
