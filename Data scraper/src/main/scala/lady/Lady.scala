package lady

class Lady(var name: String, var age: Int, var weight: Int, var height: Int, var price: Int, var isWorkingNow: Boolean) {

  def calculateBMI(): Int = {
    weight / ((height * height) / 10000)
  }

  override def toString: String =
    s"($name, age: $age, weight: $weight, height: $height, price: $price, isWorkingNow: $isWorkingNow)"
}
