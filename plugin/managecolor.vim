if !has("python3")
    echo "vim has to be compiled with +python3 to run this"
    finish
endif

" if exists('g:manacoloplugin_loaded')
"     finish
" endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" Config
if !exists('g:colo_cache_file')
	let g:colo_cache_file = resolve(s:plugin_root_dir . '/../cache/colos.json')
endif
if !exists('g:colo_search_path')
	let g:colo_search_path = resolve(s:plugin_root_dir . '/../../../../')
endif

" Load out module
python << EOF

import os
import sys
import vim

plugin_path = vim.eval("s:plugin_root_dir")
python_module_path = os.path.abspath('%s/../lib'%(plugin_path))
sys.path.append(python_module_path)

# Load the cmds functions into global space
import cmds as cololib

csdata = cololib.cmd_load_data(vim.eval('g:colo_cache_file'), verbose=False)

EOF


function! Build_colo_cache()
	python cololib.cmd_build_cache(csdata, vim.eval('g:colo_search_path'))
endfunction

function! Get_random_colo(tag)
	redir => out
	silent! python cololib.cmd_get_random_colo(csdata, vim.eval('a:tag'))
	redir END

	if (v:version >= 800 || has('nvim'))
		let out = trim(out)
	else
		let out = substitute(out, '^\s*\(.\{-}\)\s*$', '\1', '')
	endif

	exec 'colo ' . out
endfunction

function! Testme()
	python print("cache = %s"%my_var)
endfunction


" Default mappings
:map <Leader>wcs :call Get_random_colo('whitelist')<CR>
:map <Leader>rcs :call Get_random_colo('')<CR>


let g:manacoloplugin_loaded = 1

" vim: ts=4 sts=4 sw=4 noet nowrap ffs=unix :
