<?php

namespace App\Http\Controllers\API\V1;

use App\Http\Controllers\Controller;
use App\Http\Resources\V1\StateResource;
use App\Models\State;
use Illuminate\Http\Request;

class StateController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return StateResource::collection(State::all());
    }

    /**
     * Display the specified resource.
     */
    public function show(State $state)
    {
        return new StateResource($state);
    }
    
}
