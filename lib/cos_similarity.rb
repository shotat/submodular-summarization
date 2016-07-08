require 'natto'
require 'matrix'

# SEE: http://altarf.net/computer/ruby/3226

class CosSimilarity

  def self.calculate(text1, text2)
    a1 = break_up(text1)
    a2 = break_up(text2)
    return 0 if a1.length == 0 || a2.length == 0
    uniq_words = (a1 + a2).uniq

    f1 = make_flags(uniq_words, a1)
    f2 = make_flags(uniq_words, a2)

    v1 = Vector.elements(f1, copy = true)
    v2 = Vector.elements(f2, copy = true)

    return v2.inner_product(v1)/(v1.norm() * v2.norm())
  end

  private

  def self.break_up(text)
    arr = Array.new
    nm = Natto::MeCab.new
    nm.parse(text) do |n|
      surface = n.surface
      feature = n.feature.split(',')

      # 品詞が名刺、かつ記号っぽくなければ採用
      if feature.first == "名詞" && feature.last != '*'
        arr.push(surface)
      end
    end
    arr
  end

  def self.make_flags(uniq_words, elements)
    frags = []
    uniq_words.each do |word|
      flag = elements.include?(word) == true ? 1 : 0
      frags.push(flag)
    end
    frags
  end
end
