require_relative './cos_similarity.rb'

class DocSubmodular
  attr_reader :texts, :len

  def initialize(texts, params = {})
    @gumma = params[:gumma] || 0.5

    @texts = texts
    @len = @texts.length
    @memo = Array.new(@len){ Array.new(@len, -1) }
    @v_vec = Array.new(@len, 1)
    @mean_length = @texts.join.length / @len
  end
  # fdoc
  def calculate(s)
    #_lambda = 0.2
    relevance(s)#  + _lambda * redundancy
  end

  def cost(i)
    10
  end

  def cost_sum(s)
    return 0 if s.empty?
    s.reduce do |acc, idx|
      acc + cost(idx)
    end
  end

  private

  def zero_vec
  end

  def s_vec_gen(s)
    z = Array.new(@len, 0)
    s.each do |i|
      z[i] = 1
    end
    z
  end

  # L(S) relevance
  def relevance(s)
    s_vec = s_vec_gen(s)
    acc = 0
    @len.times do |i|
      s_r = cover(i, s_vec)
      v_r = @gumma * cover(i, @v_vec)
      puts "#{s_r}, #{v_r}"
      result = [s_r, v_r].min
      acc += result
    end
    acc
  end

  # R(S) redundancy
  def redundancy(s)

  end

  # C(S)
  def cover(sentence_num, set_vec)
    sentence = @texts[sentence_num]
    acc = 0
    set_vec.each_with_index do |elem, idx|
      next if elem == 0
      if @memo[sentence_num][idx] < 0
        r = CosSimilarity.calculate(sentence, @texts[idx])
        @memo[sentence_num][idx] = r
        @memo[idx][sentence_num] = r
      end
      acc += @memo[sentence_num][idx]
    end
    acc
  end
end
