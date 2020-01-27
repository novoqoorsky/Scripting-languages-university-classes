package data

import breeze.linalg.sum
import lady.Lady

import scala.collection.mutable
import scala.collection.mutable.ListBuffer

class DataCalculations {

  def mapAgeToAveragePrice(ladies: Array[Lady]): mutable.TreeMap[Int, Int] = {
    val ageToPrices = new mutable.HashMap[Int, ListBuffer[Int]]()
    ladies.foreach {
      lady => {
        if (ageToPrices.contains(lady.age)) {
          ageToPrices(lady.age).addOne(lady.price)
        } else {
          val listBuffer = new ListBuffer[Int]
          listBuffer.addOne(lady.price)
          ageToPrices.addOne(lady.age, listBuffer)
        }
      }
    }
    calculateAverage(ageToPrices)
  }

  def mapWeightToAveragePrice(ladies: Array[Lady]): mutable.TreeMap[Int, Int] = {
    val weightToPrices = new mutable.HashMap[Int, ListBuffer[Int]]()
    ladies.foreach {
      lady => {
        if (weightToPrices.contains(lady.weight)) {
          weightToPrices(lady.weight).addOne(lady.price)
        } else {
          val listBuffer = new ListBuffer[Int]
          listBuffer.addOne(lady.price)
          weightToPrices.addOne(lady.weight, listBuffer)
        }
      }
    }
    calculateAverage(weightToPrices)
  }

  def mapBMIToAveragePrice(ladies: Array[Lady]): mutable.TreeMap[Int, Int] = {
    val bmiToPrices = new mutable.HashMap[Int, ListBuffer[Int]]()
    ladies.foreach {
      lady => {
        if (bmiToPrices.contains(lady.calculateBMI())) {
          bmiToPrices(lady.calculateBMI()).addOne(lady.price)
        } else {
          val listBuffer = new ListBuffer[Int]
          listBuffer.addOne(lady.price)
          bmiToPrices.addOne(lady.calculateBMI(), listBuffer)
        }
      }
    }
    calculateAverage(bmiToPrices)
  }

  def calculateAverage(keyToArray : mutable.HashMap[Int, ListBuffer[Int]]): mutable.TreeMap[Int, Int] = {
    val keyToAverage = new mutable.TreeMap[Int, Int]
    for ((k,v) <- keyToArray) {
      keyToAverage.put(k, sum(v) / v.length)
    }
    keyToAverage
  }

  def priceHistogram(ladies: Array[Lady]): mutable.TreeMap[Int, Int] = {
    val prices = new mutable.TreeMap[Int, Int]()
    ladies.foreach {
      lady => {
        prices.updateWith(lady.price)({
          case Some(count) => Some(count + 1)
          case None => Some(1)
        })
      }
    }
    prices.map { case (k, v) => k -> (v * 100 + ladies.length - 1) / ladies.length}
  }

  def ageHistogram(ladies: Array[Lady]): mutable.TreeMap[Int, Int] = {
    val ages = new mutable.TreeMap[Int, Int]()
    ladies.foreach {
      lady => {
        ages.updateWith(lady.age)({
          case Some(count) => Some(count + 1)
          case None => Some(1)
        })
      }
    }
    ages.map { case (k, v) => k -> (v * 100 + ladies.length - 1) / ladies.length}
  }

  def weightHistogram(ladies: Array[Lady]): mutable.TreeMap[Int, Int] = {
    val weights = new mutable.TreeMap[Int, Int]()
    ladies.foreach {
      lady => {
        weights.updateWith(lady.weight)({
          case Some(count) => Some(count + 1)
          case None => Some(1)
        })
      }
    }
    weights.map { case (k, v) => k -> (v * 100 + ladies.length - 1) / ladies.length}
  }
}
