-- /home/matt/workspace/vim-managecolor/lua/managecolor/random.lua

local M = {}

function M.set_random_colo(collection_name)
  local scheme_to_set

  -- Check if a specific collection (like "whitelist") was requested.
  if collection_name and collection_name ~= "" and collection_name ~= "all" then

    -- LOGIC BRANCH 1: Use the user's config directly. DO NOT validate.
    local config = require("managecolor").config
    -- This now correctly reads from 'config.collections'
    local schemes_in_collection = config.collections and config.collections[collection_name] or {}

    if not schemes_in_collection or #schemes_in_collection == 0 then
      vim.notify("managecolor: No schemes found in your '" .. collection_name .. "' collection config.", vim.log.levels.WARN)
      return
    end

    math.randomseed(os.time())
    scheme_to_set = schemes_in_collection[math.random(#schemes_in_collection)]

  else

    -- LOGIC BRANCH 2: No collection specified. Fall back to the cache of all installed schemes.
    local json = require("managecolor.json")
    local cache_file = vim.g.colo_cache_file or vim.fn.stdpath("cache") .. "/colos.json"
    local file = io.open(cache_file, "r")
    if not file then
      vim.notify("managecolor: Cache file not found. Run :BuildColoCache", vim.log.levels.ERROR)
      return
    end

    local content = file:read("*a")
    file:close()
    local all_installed_schemes = json.decode(content)

    local eligible_schemes = {}
    for name, _ in pairs(all_installed_schemes) do
      table.insert(eligible_schemes, name)
    end

    if #eligible_schemes == 0 then
      vim.notify("managecolor: No colorschemes found in cache.", vim.log.levels.WARN)
      return
    end

    math.randomseed(os.time())
    scheme_to_set = eligible_schemes[math.random(#eligible_schemes)]
  end

  -- Apply the selected scheme. Let Neovim handle the error if it's not found.
  if scheme_to_set then
    vim.cmd('colorscheme ' .. scheme_to_set)
  end
end

return M
