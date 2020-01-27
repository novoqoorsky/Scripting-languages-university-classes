package lady

import scala.util.Try
import scala.util.matching.Regex

class LadyParametersExtractor {

  def parseName(advertisement: String): String = {
    parseParameter(advertisement, new Regex("<div class=\"podpis\">\\n(.*?)\\n"))
  }

  def parseAge(advertisement: String): Option[Int] = {
    Try(parseParameter(advertisement, new Regex("age: (\\d+)")).toInt).toOption
  }

  def parseWeight(advertisement: String): Option[Int] = {
    Try(parseParameter(advertisement, new Regex("weight: (\\d+)")).toInt).toOption
  }

  def parseHeight(advertisement: String): Option[Int] = {
    Try(parseParameter(advertisement, new Regex("height: (\\d+)")).toInt).toOption
  }

  def parsePrice(advertisement: String): Option[Int] = {
    Try(parseParameter(advertisement, new Regex("alt=\"price\"> (\\d+)")).toInt).toOption
  }

  def parseIsWorkingNow(advertisement: String): Boolean = {
    !new Regex("not working now").matches(advertisement)
  }

  def parseParameter(advertisement: String, regex: Regex): String = {
    var result: String = ""
    regex.findAllIn(advertisement).matchData foreach {
      m => result = m.group(1).trim
    }
    result
  }
}
