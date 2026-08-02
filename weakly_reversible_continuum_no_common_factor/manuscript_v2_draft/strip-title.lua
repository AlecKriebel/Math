local first_header = true

function Header(element)
  if first_header and element.level == 1 then
    first_header = false
    return {}
  end
  first_header = false
  element.level = math.max(1, element.level - 1)
  return element
end

