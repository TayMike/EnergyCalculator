<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use App\Models\FeeList;

class FeeListController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $states = FeeList::all();
        // $states = DB::select('select * from states');
 
        return view('simulador', ['states' => $states]);
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        //
    }
}
