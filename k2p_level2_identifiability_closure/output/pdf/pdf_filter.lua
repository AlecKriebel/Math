local function escaped_tex(s)
  return s:gsub("([%%#$&_{}])", "\\%1")
end

function Code(el)
  if el.text:match("^[0-9a-f]+$") and #el.text >= 32 then
    return pandoc.RawInline("latex", "\\texttt{\\seqsplit{" .. escaped_tex(el.text) .. "}}")
  end
  return el
end

function Str(el)
  if el.text == "∎" then
    return pandoc.RawInline("latex", "\\ensuremath{\\square}")
  end
  return el
end

function Math(el)
  if el.text:find("primary certificate file SHA%-256", 1, false) then
    local hashes = {}
    for hash in el.text:gmatch("texttt%{([0-9a-f]+)%}") do
      table.insert(hashes, hash)
    end
    if #hashes == 7 then
      local labels = {
        "Primary certificate file SHA-256",
        "Primary payload SHA-256",
        "Independent replay file SHA-256",
        "Independent replay payload SHA-256",
        "Mutation report file SHA-256",
        "Mutation report payload SHA-256",
        "Combined ordered-ledger root",
      }
      local lines = {
        "\\begin{center}",
        "\\begin{minipage}{0.94\\linewidth}",
        "\\small",
      }
      for i, label in ipairs(labels) do
        table.insert(lines, "\\textbf{" .. label .. "}\\\\[-1pt]")
        table.insert(lines, "\\texttt{\\seqsplit{" .. hashes[i] .. "}}\\\\[3pt]")
      end
      table.insert(lines, "\\textbf{One-port directed rows:} 29,964\\qquad " ..
                          "\\textbf{Two-port directed rows:} 544,571\\hfill (7.1)")
      table.insert(lines, "\\end{minipage}")
      table.insert(lines, "\\end{center}")
      return pandoc.RawInline("latex", table.concat(lines, "\n"))
    end
  end
  el.text = el.text:gsub([[\setminus]], [[\smallsetminus]])
  el.text = el.text:gsub([[_(\%a+)]], "_{%1}")
  el.text = el.text:gsub([[%^((\%a+))]], "^{%1}")
  return el
end

local removed_document_title = false

function Header(el)
  local label = pandoc.utils.stringify(el.content)
  if not removed_document_title and el.level == 1 and
     label == "Generic identifiability and directed containment for strongly tree-child level-2 networks under K2P" then
    removed_document_title = true
    return {}
  end
  if removed_document_title and el.level > 1 then
    el.level = el.level - 1
  end
  return el
end

