-- lua/managecolor/cache.lua

local M = {}

function M.build_cache()
  local schemes = {}
  local paths = vim.fn.globpath(vim.o.runtimepath, "colors/*.vim", true, true)

  for _, path in ipairs(paths) do
    local name = vim.fn.fnamemodify(path, ":t:r")
    if not schemes[name] then
      schemes[name] = {
        path = path,
      }
    end
  end

  local cache_file = vim.g.colo_cache_file or vim.fn.stdpath("cache") .. "/colos.json"
  local cache_dir = vim.fn.fnamemodify(cache_file, ":h")

  if vim.fn.isdirectory(cache_dir) == 0 then
    vim.fn.mkdir(cache_dir, "p")
  end

  local file = io.open(cache_file, "w")
  if file then
    file:write(vim.fn.json_encode(schemes))
    file:close()
    vim.notify("managecolor: Built cache with " .. #paths .. " colorschemes.", vim.log.levels.INFO)
  else
    vim.notify("managecolor: Could not write to cache file: " .. cache_file, vim.log.levels.ERROR)
  end
end

return M
