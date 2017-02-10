# Agisoft_automated_workflow

For the test case given to me by Bryony, the Densepointcloud build step took the longest amount of time.
On my mac, using the windows partition, that step reported the following performance characteristics for around 49 photos

```
Device 1: 100% work done with performance: 27.1 million samples/sec (CPU), device used for 1559.03 seconds
```

On Sharc, I used 118 photos and got the following performance characteristics on a  16 core node

```
Device 1: 100% work done with performance: 34.3424 million samples/sec (CPU), device used for 3392.16 seconds
```

Using 40 cores on the DGX-1 node (usually not available for this type of work), I got

```
Device 1: 100% work done with performance: 47.5967 million samples/sec (CPU), device used for 2480.54 seconds
```

Kaby Lake XPS 15 laptop using GTX 1050 GPU

```
Device 1: 6% work done with performance: 9.75637 million samples/sec (CPU), device used for 1364.09 seconds
Device 2: 93% work done with performance: 138.211 million samples/sec (GeForce GTX 1050), device used for 2748.39 seconds
Total performance: 147.968 million samples/sec
```

The GPU is clearly very useful! The time approaches that of 40 core CPUs but what I find confusing is that the performance is so much larger in terms of million samples/sec but slightly slower in terms of time taken.
