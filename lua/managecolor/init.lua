-- /home/matt/workspace/vim-managecolor/lua/managecolor/init.lua

local M = {}

-- Default configuration, using 'collections'
M.config = {
  collections = {
    whitelist = {},
  },
}

-- The all-in-one setup function
function M.setup(user_config)
  -- Merge user config with defaults
  M.config = vim.tbl_deep_extend("force", M.config, user_config or {})

  -- Create the user commands
  vim.api.nvim_create_user_command(
    "BuildColoCache",
    function()
      require("managecolor.cache").build_cache()
    end,
    {}
  )

  vim.api.nvim_create_user_command(
    "RandomColo",
    function(opts)
      require("managecolor.random").set_random_colo(opts.args)
    end,
    { nargs = "?" }
  )

  vim.api.nvim_create_user_command(
    "WhitelistColo",
    function()
      require("managecolor.random").set_random_colo("whitelist")
    end,
    {}
  )

  -- Create the keymaps
  vim.keymap.set("n", "<Leader>rcs", "<Cmd>RandomColo<CR>", { noremap = true, silent = true, desc = "Random Colorscheme" })
  vim.keymap.set("n", "<Leader>wcs", "<Cmd>WhitelistColo<CR>", { noremap = true, silent = true, desc = "Random Whitelist Colorscheme" })

  vim.notify("managecolor.nvim loaded and configured!", vim.log.levels.INFO)
end

return M
