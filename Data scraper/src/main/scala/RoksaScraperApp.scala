import data.{DataCalculations, DataVisualization}
import lady.{Lady, LadyParametersExtractor}
import net.ruippeixotog.scalascraper.browser.JsoupBrowser

import scala.collection.mutable.ListBuffer
import scala.util.matching.Regex

object RoksaScraperApp extends App {

  val browser = JsoupBrowser()

  val page = browser.get("http://roksa.pl/en/advertisements/all/Krak%C3%B3w")
  val content = page.body
  var ladies = parseLadies(divideIntoAdvertisements(content.toString))
  printMajorStats(ladies)
  plotTheData(ladies)

  def divideIntoAdvertisements(body: String): Array[String] = {
    val pattern = new Regex("<a href=\"\\/\\/www\\.roksa\\.pl\\/en\\/advertisements\\/show\\/\\d+\">((.|\\n)*?)<\\/a>")
    val advertisements =  ListBuffer[String]()
    pattern.findAllIn(body).matchData foreach {
      m => advertisements += m.group(1)
    }
    advertisements.toArray
  }

  def parseLadies(advertisements: Array[String]): Array[Lady] = {
    val ladies = ListBuffer[Lady]()
    val ladyParametersExtractor = new LadyParametersExtractor
    advertisements.foreach {
      advertisement => {
        val name = ladyParametersExtractor.parseName(advertisement)
        val age = ladyParametersExtractor.parseAge(advertisement)
        val weight = ladyParametersExtractor.parseWeight(advertisement)
        val height = ladyParametersExtractor.parseHeight(advertisement)
        val price = ladyParametersExtractor.parsePrice(advertisement)
        val isWorkingNow = ladyParametersExtractor.parseIsWorkingNow(advertisement)

        if (age.isDefined && weight.isDefined && height.isDefined && price.isDefined) {
          ladies.addOne(new Lady(name, age.get, weight.get, height.get, price.get, isWorkingNow))
        }
      }
    }
    ladies.toArray
  }

  def plotTheData(ladies: Array[Lady]): Unit = {
    val dataVisualization = new DataVisualization(new DataCalculations)
    dataVisualization.plotAll(ladies)
  }

  def printMajorStats(ladies: Array[Lady]): Unit = {
    val ladiesByPrice = ladies sortBy(_.price)
    println("The cheapest offer: " + ladiesByPrice(0).price)
    println("The most expensive offer: " + ladiesByPrice(ladies.length - 1).price)
    val ladiesByAge = ladies sortBy(_.age)
    println("The youngest lady: " +  ladiesByAge(0).age)
    println("The least young ;) lady: " +  ladiesByAge(ladies.length - 1).age)
  }
}