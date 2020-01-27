package data

import breeze.plot._
import lady.Lady

class DataVisualization(val dataCalculations: DataCalculations) {

  def plotAll(ladies: Array[Lady]): Unit = {
    val fig = new Figure("Kraków's ladies summary")
    fig.width = 1920
    fig.height = 1080
    val priceToAge = fig.subplot(3, 2, 0)
    val priceToWeight = fig.subplot(3, 2, 2)
    val priceToBMI = fig.subplot(3, 2, 4)
    val priceHistogram = fig.subplot(3, 2, 1)
    val ageHistogram = fig.subplot(3, 2, 3)
    val weightHistogram = fig.subplot(3, 2, 5)
    plotPriceToAge(ladies, priceToAge)
    plotPriceToWeight(ladies, priceToWeight)
    plotPriceToBMI(ladies, priceToBMI)
    drawPriceHistogram(ladies, priceHistogram)
    drawAgeHistogram(ladies, ageHistogram)
    drawWeightHistogram(ladies, weightHistogram)
  }

  def plotPriceToAge(ladies: Array[Lady], plt: Plot): Unit = {
    val results = dataCalculations.mapAgeToAveragePrice(ladies)
    plt += plot(results.keys.toArray, results.values.toArray)
    plt.title = "Average price with given age"
    plt.xlabel = "Age"
    plt.ylabel = "Average price"
  }

  def plotPriceToWeight(ladies: Array[Lady], plt: Plot): Unit = {
    val results = dataCalculations.mapWeightToAveragePrice(ladies)
    plt += plot(results.keys.toArray, results.values.toArray)
    plt.title = "Average price with given weight"
    plt.xlabel = "Weight"
    plt.ylabel = "Average price"
  }

  def plotPriceToBMI(ladies: Array[Lady], plt: Plot): Unit = {
    val results = dataCalculations.mapBMIToAveragePrice(ladies)
    plt += plot(results.keys.toArray, results.values.toArray)
    plt.title = "Average price with given BMI"
    plt.xlabel = "BMI"
    plt.ylabel = "Average price"
  }

  def drawPriceHistogram(ladies: Array[Lady], plt: Plot): Unit = {
    val results = dataCalculations.priceHistogram(ladies)
    plt += plot(results.keys.toArray, results.values.toArray, '+')
    plt.title = "Price histogram"
    plt.xlabel = "Price"
    plt.ylabel = "Percent of ladies"
  }

  def drawAgeHistogram(ladies: Array[Lady], plt: Plot): Unit = {
    val results = dataCalculations.ageHistogram(ladies)
    plt += plot(results.keys.toArray, results.values.toArray, '+')
    plt.title = "Age histogram"
    plt.xlabel = "Age"
    plt.ylabel = "Percent of ladies"
  }

  def drawWeightHistogram(ladies: Array[Lady], plt: Plot): Unit = {
    val results = dataCalculations.weightHistogram(ladies)
    plt += plot(results.keys.toArray, results.values.toArray, '+')
    plt.title = "Weight histogram"
    plt.xlabel = "Weight"
    plt.ylabel = "Percent of ladies"
  }
}
